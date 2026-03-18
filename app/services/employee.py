import secrets
from datetime import datetime, time, timezone

from fastapi import status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.models.employee.employee import Employee
from app.models.employee.employee_tr import EmployeeTr
from app.models.employee.contact import Contact
from app.models.employee.research import Research
from app.models.employee.office_hour import OfficeHour, DayOfWeek
from app.models.employee.education import Education, DegreeLevel
from app.models.employee.education_tr import EducationTr
from app.models.employee.teaching_course import TeachingCourse, EducationLevel
from app.models.employee.teaching_course_tr import TeachingCourseTr
from app.api.v1.schema.employee import CreateEmployee, UpdateEmployee

logger = get_logger(__name__)


def _employee_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


def _parse_time(value: str) -> time:
    try:
        parts = value.strip().split(":")
        return time(int(parts[0]), int(parts[1]))
    except Exception:
        raise ValueError(f"Invalid time format '{value}'. Expected HH:MM.")


def _check_overlap(existing: list[OfficeHour], day: str, start: time, end: time) -> bool:
    for oh in existing:
        if oh.day_of_week.value == day:
            if start < oh.end_time and end > oh.start_time:
                return True
    return False


def _format_time(t: time | None) -> str | None:
    return t.strftime("%H:%M") if t else None


def _tr_dict(tr: EmployeeTr | None) -> dict | None:
    if not tr:
        return None
    return {
        "first_name": tr.first_name,
        "last_name": tr.last_name,
        "full_name": tr.full_name,
        "academic_degree": tr.academic_degree,
        "academic_title": tr.academic_title,
        "position": tr.position,
        "scientific_interests": tr.scientific_interests,
        "biography": tr.biography,
    }


def _build_full_employee_response(emp: Employee) -> dict:
    """Build the full nested response dict from a fully-loaded Employee ORM object."""
    tr_map = {tr.lang_code: tr for tr in emp.translations}

    contact_data = None
    if emp.contact:
        c = emp.contact
        contact_data = {
            "email": c.email,
            "phone": c.phone,
            "building": c.building,
            "floor": c.floor,
            "room": c.room,
        }

    research_data = None
    if emp.research:
        r = emp.research
        research_data = {
            "scopus_url": r.scopus_url,
            "google_scholar_url": r.google_scholar_url,
            "orcid_url": r.orcid_url,
            "researchgate_url": r.researchgate_url,
            "academia_url": r.academia_url,
            "publications": r.publications,
        }

    office_hours = [
        {
            "id": oh.id,
            "day_of_week": oh.day_of_week.value,
            "start_time": _format_time(oh.start_time),
            "end_time": _format_time(oh.end_time),
        }
        for oh in emp.office_hours
    ]

    educations = []
    for e in emp.educations:
        edu_tr_map = {t.lang_code: t for t in e.translations}
        educations.append({
            "id": e.id,
            "degree_level": e.degree_level.value,
            "graduation_year": e.graduation_year,
            "institution": {
                "az": edu_tr_map["az"].institution if "az" in edu_tr_map else None,
                "en": edu_tr_map["en"].institution if "en" in edu_tr_map else None,
            },
            "specialization": {
                "az": edu_tr_map["az"].specialization if "az" in edu_tr_map else None,
                "en": edu_tr_map["en"].specialization if "en" in edu_tr_map else None,
            },
        })

    courses = []
    for c in emp.courses:
        c_tr_map = {t.lang_code: t for t in c.translations}
        courses.append({
            "id": c.id,
            "education_level": c.education_level.value,
            "course_name": {
                "az": c_tr_map["az"].course_name if "az" in c_tr_map else None,
                "en": c_tr_map["en"].course_name if "en" in c_tr_map else None,
            },
        })

    return {
        "id": emp.id,
        "employee_code": emp.employee_code,
        "profile_image": emp.profile_image,
        "faculty_code": emp.faculty_code,
        "cafedra_code": emp.cafedra_code,
        "translations": {
            "az": _tr_dict(tr_map.get("az")),
            "en": _tr_dict(tr_map.get("en")),
        },
        "contact": contact_data,
        "research": research_data,
        "office_hours": office_hours,
        "education": educations,
        "courses": courses,
        "created_at": emp.created_at.isoformat() if emp.created_at else None,
        "updated_at": emp.updated_at.isoformat() if emp.updated_at else None,
    }


def _full_load_query(where_clause):
    return (
        select(Employee)
        .options(
            selectinload(Employee.translations),
            selectinload(Employee.contact),
            selectinload(Employee.research),
            selectinload(Employee.office_hours),
            selectinload(Employee.educations).selectinload(Education.translations),
            selectinload(Employee.courses).selectinload(TeachingCourse.translations),
        )
        .where(where_clause)
    )


async def _upsert_translation(
    db: AsyncSession,
    employee_code: str,
    lang: str,
    now: datetime,
    **fields,
) -> None:
    """Upsert an EmployeeTr record for the given lang_code."""
    tr_q = await db.execute(
        select(EmployeeTr).where(
            EmployeeTr.employee_code == employee_code,
            EmployeeTr.lang_code == lang,
        )
    )
    tr = tr_q.scalar_one_or_none()
    if tr:
        for k, v in fields.items():
            if v is not None:
                setattr(tr, k, v)
        tr.updated_at = now
    else:
        db.add(EmployeeTr(
            employee_code=employee_code,
            lang_code=lang,
            created_at=now,
            **{k: v for k, v in fields.items() if v is not None},
        ))


async def create_employee(request: CreateEmployee, db: AsyncSession):
    try:
        # Generate unique employee code
        employee_code = None
        for _ in range(10):
            candidate = _employee_code_generator()
            existing = await db.execute(
                select(Employee).where(Employee.employee_code == candidate)
            )
            if not existing.scalar_one_or_none():
                employee_code = candidate
                break
        if not employee_code:
            return JSONResponse(
                content={"status_code": 500, "message": "Failed to generate unique employee code."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        now = datetime.now(timezone.utc)

        # Save profile image (required)
        profile_image_path = await save_upload(
            upload=request.profile_image,
            subdirectory="employees",
            allowed_mimes=ALLOWED_IMAGE_MIMES,
        )

        # Create base Employee record
        employee = Employee(
            employee_code=employee_code,
            profile_image=profile_image_path,
            faculty_code=request.faculty_code,
            cafedra_code=request.cafedra_code,
            created_at=now,
        )
        db.add(employee)
        await db.flush()

        # AZ translation (required)
        db.add(EmployeeTr(
            employee_code=employee_code,
            lang_code="az",
            first_name=request.first_name_az,
            last_name=request.last_name_az,
            full_name=f"{request.first_name_az} {request.last_name_az}",
            academic_degree=request.az_academic_degree,
            academic_title=request.az_academic_title,
            position=request.az_position,
            scientific_interests=request.az_scientific_interests,
            biography=request.az_biography,
            created_at=now,
        ))

        # EN translation (optional — only create if any en field is provided)
        en_fields = {
            "first_name": request.first_name_en,
            "last_name": request.last_name_en,
            "academic_degree": request.en_academic_degree,
            "academic_title": request.en_academic_title,
            "position": request.en_position,
            "scientific_interests": request.en_scientific_interests,
            "biography": request.en_biography,
        }
        if any(v is not None for v in en_fields.values()):
            fn_en = request.first_name_en or request.first_name_az
            ln_en = request.last_name_en or request.last_name_az
            db.add(EmployeeTr(
                employee_code=employee_code,
                lang_code="en",
                first_name=fn_en,
                last_name=ln_en,
                full_name=f"{fn_en} {ln_en}",
                academic_degree=request.en_academic_degree,
                academic_title=request.en_academic_title,
                position=request.en_position,
                scientific_interests=request.en_scientific_interests,
                biography=request.en_biography,
                created_at=now,
            ))

        # Contact (required)
        c = request.contact
        db.add(Contact(
            employee_code=employee_code,
            email=c["email"],
            phone=c["phone"],
            building=c["building"],
            floor=c["floor"],
            room=c["room"],
        ))

        # Research (optional)
        if request.research:
            r = request.research
            db.add(Research(
                employee_code=employee_code,
                scopus_url=r.get("scopus_url"),
                google_scholar_url=r.get("google_scholar_url"),
                orcid_url=r.get("orcid_url"),
                researchgate_url=r.get("researchgate_url"),
                academia_url=r.get("academia_url"),
                publications=r.get("publications"),
            ))

        # Office hours (min 1, with overlap check)
        submitted_hours: list[OfficeHour] = []
        errors: dict[str, list[str]] = {}
        for oh in request.office_hours:
            day = oh.get("day_of_week")
            start_str = oh.get("start_time")
            end_str = oh.get("end_time")
            if not (day and start_str and end_str):
                errors["office_hours"] = errors.get("office_hours", []) + [
                    "Each office_hour must have day_of_week, start_time, end_time."
                ]
                continue
            try:
                start_t = _parse_time(start_str)
                end_t = _parse_time(end_str)
            except ValueError as e:
                errors[f"office_hours.{day}"] = [str(e)]
                continue
            if start_t >= end_t:
                errors[f"office_hours.{day}"] = [f"start_time must be before end_time on {day}."]
                continue
            if _check_overlap(submitted_hours, day, start_t, end_t):
                errors[f"office_hours.{day}"] = [f"Time slots overlap on {day}."]
                continue
            record = OfficeHour(
                employee_code=employee_code,
                day_of_week=DayOfWeek(day),
                start_time=start_t,
                end_time=end_t,
            )
            db.add(record)
            submitted_hours.append(record)

        if errors:
            await db.rollback()
            return JSONResponse(
                content={"errors": errors},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Education (min 1)
        for edu in request.education:
            degree = edu.get("degree_level")
            if not degree:
                return JSONResponse(
                    content={"errors": {"education": ["degree_level is required for each education entry."]}},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            edu_record = Education(
                employee_code=employee_code,
                degree_level=DegreeLevel(degree),
                graduation_year=edu.get("graduation_year"),
            )
            db.add(edu_record)
            await db.flush()

            # Education translations
            if edu.get("institution_az") or edu.get("specialization_az"):
                db.add(EducationTr(
                    education_id=edu_record.id,
                    lang_code="az",
                    institution=edu.get("institution_az"),
                    specialization=edu.get("specialization_az"),
                ))
            if edu.get("institution_en") or edu.get("specialization_en"):
                db.add(EducationTr(
                    education_id=edu_record.id,
                    lang_code="en",
                    institution=edu.get("institution_en"),
                    specialization=edu.get("specialization_en"),
                ))

        # Courses (optional)
        for course in request.courses:
            level = course.get("education_level")
            if not level:
                return JSONResponse(
                    content={"errors": {"courses": ["education_level is required for each course entry."]}},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            course_record = TeachingCourse(
                employee_code=employee_code,
                education_level=EducationLevel(level),
            )
            db.add(course_record)
            await db.flush()

            if course.get("course_name_az"):
                db.add(TeachingCourseTr(
                    course_id=course_record.id,
                    lang_code="az",
                    course_name=course["course_name_az"],
                ))
            if course.get("course_name_en"):
                db.add(TeachingCourseTr(
                    course_id=course_record.id,
                    lang_code="en",
                    course_name=course["course_name_en"],
                ))

        await db.commit()

        # Fetch full response
        emp_q = await db.execute(_full_load_query(Employee.employee_code == employee_code))
        emp = emp_q.scalar_one()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Employee created successfully.",
                "data": _build_full_employee_response(emp),
            },
            status_code=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"errors": {"validation": [str(e)]}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        await db.rollback()
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_employees(
    start: int,
    end: int,
    lang: str,
    db: AsyncSession,
    faculty_code: str | None = None,
    cafedra_code: str | None = None,
):
    try:
        count_stmt = select(func.count()).select_from(Employee)
        list_stmt = (
            select(Employee)
            .options(selectinload(Employee.translations))
        )

        if faculty_code:
            count_stmt = count_stmt.where(Employee.faculty_code == faculty_code)
            list_stmt = list_stmt.where(Employee.faculty_code == faculty_code)
        if cafedra_code:
            count_stmt = count_stmt.where(Employee.cafedra_code == cafedra_code)
            list_stmt = list_stmt.where(Employee.cafedra_code == cafedra_code)

        total = (await db.execute(count_stmt)).scalar() or 0
        employees = (
            await db.execute(list_stmt.order_by(Employee.id.asc()).offset(start).limit(end - start))
        ).scalars().all()

        if not employees:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        result = []
        for emp in employees:
            tr_map = {tr.lang_code: tr for tr in emp.translations}
            tr = tr_map.get(lang) or tr_map.get("az")
            result.append({
                "id": emp.id,
                "employee_code": emp.employee_code,
                "profile_image": emp.profile_image,
                "faculty_code": emp.faculty_code,
                "cafedra_code": emp.cafedra_code,
                "first_name": tr.first_name if tr else None,
                "last_name": tr.last_name if tr else None,
                "full_name": tr.full_name if tr else None,
                "academic_degree": tr.academic_degree if tr else None,
                "academic_title": tr.academic_title if tr else None,
                "position": tr.position if tr else None,
                "biography": tr.biography if tr else None,
                "created_at": emp.created_at.isoformat() if emp.created_at else None,
                "updated_at": emp.updated_at.isoformat() if emp.updated_at else None,
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Employees fetched successfully.",
                "employees": result,
                "total": total,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_employee(employee_code: str, lang_code: str, db: AsyncSession):
    try:
        emp_q = await db.execute(_full_load_query(Employee.employee_code == employee_code))
        emp = emp_q.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Employee details fetched successfully.",
                "employee": _build_full_employee_response(emp),
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_employee(employee_code: str, request: UpdateEmployee, db: AsyncSession):
    try:
        emp_q = await db.execute(
            _full_load_query(Employee.employee_code == employee_code)
        )
        emp = emp_q.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)

        # Update base fields
        if request.faculty_code is not None:
            emp.faculty_code = request.faculty_code
        if request.cafedra_code is not None:
            emp.cafedra_code = request.cafedra_code

        # Profile image
        if request.profile_image and request.profile_image.filename:
            old_image = emp.profile_image
            emp.profile_image = await save_upload(
                upload=request.profile_image,
                subdirectory="employees",
                allowed_mimes=ALLOWED_IMAGE_MIMES,
            )
            if old_image:
                safe_delete_file(old_image)

        # AZ translation upsert
        az_fields = {
            "first_name": request.first_name_az,
            "last_name": request.last_name_az,
            "academic_degree": request.az_academic_degree,
            "academic_title": request.az_academic_title,
            "position": request.az_position,
            "scientific_interests": request.az_scientific_interests,
            "biography": request.az_biography,
        }
        if any(v is not None for v in az_fields.values()):
            await _upsert_translation(db, employee_code, "az", now, **az_fields)
            # Recompute full_name if names changed
            tr_az_q = await db.execute(
                select(EmployeeTr).where(
                    EmployeeTr.employee_code == employee_code,
                    EmployeeTr.lang_code == "az",
                )
            )
            tr_az = tr_az_q.scalar_one_or_none()
            if tr_az and tr_az.first_name and tr_az.last_name:
                tr_az.full_name = f"{tr_az.first_name} {tr_az.last_name}"

        # EN translation upsert
        en_fields = {
            "first_name": request.first_name_en,
            "last_name": request.last_name_en,
            "academic_degree": request.en_academic_degree,
            "academic_title": request.en_academic_title,
            "position": request.en_position,
            "scientific_interests": request.en_scientific_interests,
            "biography": request.en_biography,
        }
        if any(v is not None for v in en_fields.values()):
            await _upsert_translation(db, employee_code, "en", now, **en_fields)
            tr_en_q = await db.execute(
                select(EmployeeTr).where(
                    EmployeeTr.employee_code == employee_code,
                    EmployeeTr.lang_code == "en",
                )
            )
            tr_en = tr_en_q.scalar_one_or_none()
            if tr_en and tr_en.first_name and tr_en.last_name:
                tr_en.full_name = f"{tr_en.first_name} {tr_en.last_name}"

        # Contact upsert
        if request.contact is not None:
            c = request.contact
            if emp.contact:
                emp.contact.email = c["email"]
                emp.contact.phone = c["phone"]
                emp.contact.building = c["building"]
                emp.contact.floor = c["floor"]
                emp.contact.room = c["room"]
            else:
                db.add(Contact(
                    employee_code=employee_code,
                    email=c["email"],
                    phone=c["phone"],
                    building=c["building"],
                    floor=c["floor"],
                    room=c["room"],
                ))

        # Research upsert
        if request.research is not None:
            r = request.research
            if emp.research:
                emp.research.scopus_url = r.get("scopus_url", emp.research.scopus_url)
                emp.research.google_scholar_url = r.get("google_scholar_url", emp.research.google_scholar_url)
                emp.research.orcid_url = r.get("orcid_url", emp.research.orcid_url)
                emp.research.researchgate_url = r.get("researchgate_url", emp.research.researchgate_url)
                emp.research.academia_url = r.get("academia_url", emp.research.academia_url)
                emp.research.publications = r.get("publications", emp.research.publications)
            else:
                db.add(Research(
                    employee_code=employee_code,
                    scopus_url=r.get("scopus_url"),
                    google_scholar_url=r.get("google_scholar_url"),
                    orcid_url=r.get("orcid_url"),
                    researchgate_url=r.get("researchgate_url"),
                    academia_url=r.get("academia_url"),
                    publications=r.get("publications"),
                ))

        # Office hours: replace all if provided
        if request.office_hours is not None:
            await db.execute(
                sqlalchemy_delete(OfficeHour).where(OfficeHour.employee_code == employee_code)
            )
            submitted: list[OfficeHour] = []
            errors: dict[str, list[str]] = {}
            for oh in request.office_hours:
                day = oh.get("day_of_week")
                try:
                    start_t = _parse_time(oh["start_time"])
                    end_t = _parse_time(oh["end_time"])
                except (ValueError, KeyError) as e:
                    errors[f"office_hours.{day}"] = [str(e)]
                    continue
                if start_t >= end_t:
                    errors[f"office_hours.{day}"] = [f"start_time must be before end_time on {day}."]
                    continue
                if _check_overlap(submitted, day, start_t, end_t):
                    errors[f"office_hours.{day}"] = [f"Time slots overlap on {day}."]
                    continue
                record = OfficeHour(
                    employee_code=employee_code,
                    day_of_week=DayOfWeek(day),
                    start_time=start_t,
                    end_time=end_t,
                )
                db.add(record)
                submitted.append(record)
            if errors:
                await db.rollback()
                return JSONResponse(content={"errors": errors}, status_code=status.HTTP_400_BAD_REQUEST)

        # Education: replace all if provided
        if request.education is not None:
            existing_edu = (await db.execute(
                select(Education).where(Education.employee_code == employee_code)
            )).scalars().all()
            for e in existing_edu:
                await db.execute(sqlalchemy_delete(EducationTr).where(EducationTr.education_id == e.id))
            await db.execute(sqlalchemy_delete(Education).where(Education.employee_code == employee_code))

            for edu in request.education:
                degree = edu.get("degree_level")
                if not degree:
                    await db.rollback()
                    return JSONResponse(
                        content={"errors": {"education": ["degree_level is required for each education entry."]}},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                edu_record = Education(
                    employee_code=employee_code,
                    degree_level=DegreeLevel(degree),
                    graduation_year=edu.get("graduation_year"),
                )
                db.add(edu_record)
                await db.flush()
                if edu.get("institution_az") or edu.get("specialization_az"):
                    db.add(EducationTr(
                        education_id=edu_record.id,
                        lang_code="az",
                        institution=edu.get("institution_az"),
                        specialization=edu.get("specialization_az"),
                    ))
                if edu.get("institution_en") or edu.get("specialization_en"):
                    db.add(EducationTr(
                        education_id=edu_record.id,
                        lang_code="en",
                        institution=edu.get("institution_en"),
                        specialization=edu.get("specialization_en"),
                    ))

        # Courses: replace all if provided
        if request.courses is not None:
            existing_courses = (await db.execute(
                select(TeachingCourse).where(TeachingCourse.employee_code == employee_code)
            )).scalars().all()
            for c in existing_courses:
                await db.execute(sqlalchemy_delete(TeachingCourseTr).where(TeachingCourseTr.course_id == c.id))
            await db.execute(sqlalchemy_delete(TeachingCourse).where(TeachingCourse.employee_code == employee_code))

            for course in request.courses:
                level = course.get("education_level")
                if not level:
                    await db.rollback()
                    return JSONResponse(
                        content={"errors": {"courses": ["education_level is required for each course entry."]}},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                course_record = TeachingCourse(
                    employee_code=employee_code,
                    education_level=EducationLevel(level),
                )
                db.add(course_record)
                await db.flush()
                if course.get("course_name_az"):
                    db.add(TeachingCourseTr(course_id=course_record.id, lang_code="az", course_name=course["course_name_az"]))
                if course.get("course_name_en"):
                    db.add(TeachingCourseTr(course_id=course_record.id, lang_code="en", course_name=course["course_name_en"]))

        emp.updated_at = now
        await db.commit()

        emp_q = await db.execute(_full_load_query(Employee.employee_code == employee_code))
        emp = emp_q.scalar_one()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Employee updated successfully.",
                "data": _build_full_employee_response(emp),
            },
            status_code=status.HTTP_200_OK,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"errors": {"validation": [str(e)]}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        await db.rollback()
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_employee(employee_code: str, db: AsyncSession):
    try:
        emp_q = await db.execute(
            select(Employee)
            .options(selectinload(Employee.educations), selectinload(Employee.courses))
            .where(Employee.employee_code == employee_code)
        )
        emp = emp_q.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Delete profile image file
        if emp.profile_image:
            safe_delete_file(emp.profile_image)

        # Delete child translations before deleting parents (FK cascade may not cover cross-table)
        for e in emp.educations:
            await db.execute(sqlalchemy_delete(EducationTr).where(EducationTr.education_id == e.id))
        for c in emp.courses:
            await db.execute(sqlalchemy_delete(TeachingCourseTr).where(TeachingCourseTr.course_id == c.id))

        # Delete employee (cascades: employee_tr, contact, research, office_hours, education, courses)
        await db.execute(sqlalchemy_delete(Employee).where(Employee.employee_code == employee_code))
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception:
        await db.rollback()
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
