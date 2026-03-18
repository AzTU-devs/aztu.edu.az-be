import secrets
from datetime import datetime, time, timezone

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.core.logger import get_logger
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.models.employee.employee import Employee
from app.models.employee.employee_tr import EmployeeTr
from app.models.employee.office_hour import OfficeHour, DayOfWeek
from app.models.employee.education import Education, DegreeLevel
from app.models.employee.teaching_course import TeachingCourse, EducationLevel
from app.api.v1.schema.employee import CreateEmployee, UpdateEmployee

logger = get_logger(__name__)


def employee_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


def _parse_time(value: str) -> time:
    """Parse HH:MM string to datetime.time."""
    try:
        parts = value.strip().split(":")
        return time(int(parts[0]), int(parts[1]))
    except Exception:
        raise ValueError(f"Invalid time format '{value}'. Expected HH:MM.")


def _check_overlap(existing: list[OfficeHour], day: str, start: time, end: time) -> bool:
    """Return True if the given slot overlaps with any existing slot for the same day."""
    for oh in existing:
        if oh.day_of_week.value == day:
            if start < oh.end_time and end > oh.start_time:
                return True
    return False


def _format_time(t: time | None) -> str | None:
    if t is None:
        return None
    return t.strftime("%H:%M")


async def create_employee(
    request: CreateEmployee,
    db: AsyncSession,
):
    try:
        employee_code = None
        for _ in range(10):
            candidate = employee_code_generator()
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

        # Handle profile image upload
        profile_image_path = None
        if request.profile_image and request.profile_image.filename:
            profile_image_path = await save_upload(
                upload=request.profile_image,
                subdirectory="employees",
                allowed_mimes=ALLOWED_IMAGE_MIMES,
            )

        employee = Employee(
            employee_code=employee_code,
            first_name=request.first_name,
            last_name=request.last_name,
            full_name=request.full_name,
            profile_image=profile_image_path,
            academic_degree=request.academic_degree,
            academic_title=request.academic_title,
            position=request.position,
            faculty_code=request.faculty_code,
            cafedra_code=request.cafedra_code,
            email=request.email,
            phone=request.phone,
            building=request.building,
            floor=request.floor,
            room=request.room,
            scopus_url=request.scopus_url,
            google_scholar_url=request.google_scholar_url,
            orcid_url=request.orcid_url,
            researchgate_url=request.researchgate_url,
            academia_url=request.academia_url,
            scientific_interests=request.scientific_interests,
            publications=request.publications,
            created_at=now,
        )
        db.add(employee)
        await db.flush()  # get employee_code into DB before adding relations

        # Biography translations
        if request.az_biography is not None:
            db.add(EmployeeTr(
                employee_code=employee_code,
                lang_code="az",
                biography=request.az_biography,
                created_at=now,
            ))
        if request.en_biography is not None:
            db.add(EmployeeTr(
                employee_code=employee_code,
                lang_code="en",
                biography=request.en_biography,
                created_at=now,
            ))

        # Office hours (with overlap check within the submitted list)
        submitted_hours: list[OfficeHour] = []
        for oh in request.office_hours:
            day = oh.get("day_of_week")
            start_str = oh.get("start_time")
            end_str = oh.get("end_time")
            if not (day and start_str and end_str):
                return JSONResponse(
                    content={"status_code": 400, "message": "Each office_hour must have day_of_week, start_time, end_time."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            start_t = _parse_time(start_str)
            end_t = _parse_time(end_str)
            if start_t >= end_t:
                return JSONResponse(
                    content={"status_code": 400, "message": f"start_time must be before end_time for {day}."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            if _check_overlap(submitted_hours, day, start_t, end_t):
                return JSONResponse(
                    content={"status_code": 400, "message": f"Office hours overlap on {day}."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            record = OfficeHour(
                employee_code=employee_code,
                day_of_week=DayOfWeek(day),
                start_time=start_t,
                end_time=end_t,
            )
            db.add(record)
            submitted_hours.append(record)

        # Education records
        for edu in request.education:
            db.add(Education(
                employee_code=employee_code,
                degree_level=DegreeLevel(edu["degree_level"]),
                institution=edu["institution"],
                specialization=edu.get("specialization"),
                graduation_year=edu.get("graduation_year"),
            ))

        # Teaching courses
        for course in request.courses:
            db.add(TeachingCourse(
                employee_code=employee_code,
                course_name=course["course_name"],
                education_level=EducationLevel(course["education_level"]),
            ))

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Employee created successfully.",
                "data": {
                    "employee_code": employee_code,
                    "full_name": request.full_name,
                    "created_at": now.isoformat(),
                },
            },
            status_code=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 400, "message": str(e)},
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
        list_stmt = select(Employee)

        if faculty_code:
            count_stmt = count_stmt.where(Employee.faculty_code == faculty_code)
            list_stmt = list_stmt.where(Employee.faculty_code == faculty_code)
        if cafedra_code:
            count_stmt = count_stmt.where(Employee.cafedra_code == cafedra_code)
            list_stmt = list_stmt.where(Employee.cafedra_code == cafedra_code)

        total_query = await db.execute(count_stmt)
        total = total_query.scalar() or 0

        employees_query = await db.execute(
            list_stmt.order_by(Employee.id.asc()).offset(start).limit(end - start)
        )
        employees = employees_query.scalars().all()

        if not employees:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        result = []
        for emp in employees:
            tr_query = await db.execute(
                select(EmployeeTr).where(
                    EmployeeTr.employee_code == emp.employee_code,
                    EmployeeTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()

            result.append({
                "id": emp.id,
                "employee_code": emp.employee_code,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "full_name": emp.full_name,
                "profile_image": emp.profile_image,
                "academic_degree": emp.academic_degree,
                "academic_title": emp.academic_title,
                "position": emp.position,
                "faculty_code": emp.faculty_code,
                "cafedra_code": emp.cafedra_code,
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


async def get_employee(
    employee_code: str,
    lang_code: str,
    db: AsyncSession,
):
    try:
        emp_query = await db.execute(
            select(Employee).where(Employee.employee_code == employee_code)
        )
        emp = emp_query.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Translations (both languages for full detail)
        az_tr_q = await db.execute(
            select(EmployeeTr).where(
                EmployeeTr.employee_code == employee_code,
                EmployeeTr.lang_code == "az",
            )
        )
        az_tr = az_tr_q.scalar_one_or_none()

        en_tr_q = await db.execute(
            select(EmployeeTr).where(
                EmployeeTr.employee_code == employee_code,
                EmployeeTr.lang_code == "en",
            )
        )
        en_tr = en_tr_q.scalar_one_or_none()

        # Office hours
        oh_query = await db.execute(
            select(OfficeHour).where(OfficeHour.employee_code == employee_code)
        )
        office_hours = [
            {
                "id": oh.id,
                "day_of_week": oh.day_of_week.value,
                "start_time": _format_time(oh.start_time),
                "end_time": _format_time(oh.end_time),
            }
            for oh in oh_query.scalars().all()
        ]

        # Education
        edu_query = await db.execute(
            select(Education).where(Education.employee_code == employee_code)
        )
        education = [
            {
                "id": e.id,
                "degree_level": e.degree_level.value,
                "institution": e.institution,
                "specialization": e.specialization,
                "graduation_year": e.graduation_year,
            }
            for e in edu_query.scalars().all()
        ]

        # Courses
        course_query = await db.execute(
            select(TeachingCourse).where(TeachingCourse.employee_code == employee_code)
        )
        courses = [
            {
                "id": c.id,
                "course_name": c.course_name,
                "education_level": c.education_level.value,
            }
            for c in course_query.scalars().all()
        ]

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Employee details fetched successfully.",
                "employee": {
                    "employee_code": emp.employee_code,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "profile_image": emp.profile_image,
                    "academic_degree": emp.academic_degree,
                    "academic_title": emp.academic_title,
                    "position": emp.position,
                    "faculty_code": emp.faculty_code,
                    "cafedra_code": emp.cafedra_code,
                    "email": emp.email,
                    "phone": emp.phone,
                    "building": emp.building,
                    "floor": emp.floor,
                    "room": emp.room,
                    "scopus_url": emp.scopus_url,
                    "google_scholar_url": emp.google_scholar_url,
                    "orcid_url": emp.orcid_url,
                    "researchgate_url": emp.researchgate_url,
                    "academia_url": emp.academia_url,
                    "scientific_interests": emp.scientific_interests,
                    "publications": emp.publications,
                    "biography": {
                        "az": az_tr.biography if az_tr else None,
                        "en": en_tr.biography if en_tr else None,
                    },
                    "office_hours": office_hours,
                    "education": education,
                    "courses": courses,
                    "created_at": emp.created_at.isoformat() if emp.created_at else None,
                    "updated_at": emp.updated_at.isoformat() if emp.updated_at else None,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_employee(
    employee_code: str,
    request: UpdateEmployee,
    db: AsyncSession,
):
    try:
        emp_query = await db.execute(
            select(Employee).where(Employee.employee_code == employee_code)
        )
        emp = emp_query.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)

        # Update scalar fields
        if request.first_name is not None:
            emp.first_name = request.first_name
        if request.last_name is not None:
            emp.last_name = request.last_name
        if request.first_name is not None or request.last_name is not None:
            emp.full_name = f"{emp.first_name} {emp.last_name}"
        if request.academic_degree is not None:
            emp.academic_degree = request.academic_degree
        if request.academic_title is not None:
            emp.academic_title = request.academic_title
        if request.position is not None:
            emp.position = request.position
        if request.faculty_code is not None:
            emp.faculty_code = request.faculty_code
        if request.cafedra_code is not None:
            emp.cafedra_code = request.cafedra_code
        if request.email is not None:
            emp.email = request.email
        if request.phone is not None:
            emp.phone = request.phone
        if request.building is not None:
            emp.building = request.building
        if request.floor is not None:
            emp.floor = request.floor
        if request.room is not None:
            emp.room = request.room
        if request.scopus_url is not None:
            emp.scopus_url = request.scopus_url
        if request.google_scholar_url is not None:
            emp.google_scholar_url = request.google_scholar_url
        if request.orcid_url is not None:
            emp.orcid_url = request.orcid_url
        if request.researchgate_url is not None:
            emp.researchgate_url = request.researchgate_url
        if request.academia_url is not None:
            emp.academia_url = request.academia_url
        if request.scientific_interests is not None:
            emp.scientific_interests = request.scientific_interests
        if request.publications is not None:
            emp.publications = request.publications

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

        # Biography upsert
        async def upsert_biography(lang: str, bio: str | None):
            if bio is None:
                return
            tr_q = await db.execute(
                select(EmployeeTr).where(
                    EmployeeTr.employee_code == employee_code,
                    EmployeeTr.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()
            if tr:
                tr.biography = bio
                tr.updated_at = now
            else:
                db.add(EmployeeTr(
                    employee_code=employee_code,
                    lang_code=lang,
                    biography=bio,
                    created_at=now,
                ))

        await upsert_biography("az", request.az_biography)
        await upsert_biography("en", request.en_biography)

        # Office hours: replace all if provided
        if request.office_hours is not None:
            await db.execute(
                sqlalchemy_delete(OfficeHour).where(OfficeHour.employee_code == employee_code)
            )
            submitted: list[OfficeHour] = []
            for oh in request.office_hours:
                day = oh.get("day_of_week")
                start_t = _parse_time(oh["start_time"])
                end_t = _parse_time(oh["end_time"])
                if start_t >= end_t:
                    return JSONResponse(
                        content={"status_code": 400, "message": f"start_time must be before end_time for {day}."},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                if _check_overlap(submitted, day, start_t, end_t):
                    return JSONResponse(
                        content={"status_code": 400, "message": f"Office hours overlap on {day}."},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                record = OfficeHour(
                    employee_code=employee_code,
                    day_of_week=DayOfWeek(day),
                    start_time=start_t,
                    end_time=end_t,
                )
                db.add(record)
                submitted.append(record)

        # Education: replace all if provided
        if request.education is not None:
            await db.execute(
                sqlalchemy_delete(Education).where(Education.employee_code == employee_code)
            )
            for edu in request.education:
                db.add(Education(
                    employee_code=employee_code,
                    degree_level=DegreeLevel(edu["degree_level"]),
                    institution=edu["institution"],
                    specialization=edu.get("specialization"),
                    graduation_year=edu.get("graduation_year"),
                ))

        # Courses: replace all if provided
        if request.courses is not None:
            await db.execute(
                sqlalchemy_delete(TeachingCourse).where(TeachingCourse.employee_code == employee_code)
            )
            for course in request.courses:
                db.add(TeachingCourse(
                    employee_code=employee_code,
                    course_name=course["course_name"],
                    education_level=EducationLevel(course["education_level"]),
                ))

        emp.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Employee updated successfully.",
                "data": {
                    "employee_code": employee_code,
                    "updated_at": now.isoformat(),
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 400, "message": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        await db.rollback()
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_employee(
    employee_code: str,
    db: AsyncSession,
):
    try:
        emp_query = await db.execute(
            select(Employee).where(Employee.employee_code == employee_code)
        )
        emp = emp_query.scalar_one_or_none()

        if not emp:
            return JSONResponse(
                content={"status_code": 404, "message": "Employee not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Delete profile image file
        if emp.profile_image:
            safe_delete_file(emp.profile_image)

        # Cascade deletes handle related tables via FK, but explicit for clarity
        await db.execute(sqlalchemy_delete(OfficeHour).where(OfficeHour.employee_code == employee_code))
        await db.execute(sqlalchemy_delete(Education).where(Education.employee_code == employee_code))
        await db.execute(sqlalchemy_delete(TeachingCourse).where(TeachingCourse.employee_code == employee_code))
        await db.execute(sqlalchemy_delete(EmployeeTr).where(EmployeeTr.employee_code == employee_code))
        await db.execute(sqlalchemy_delete(Employee).where(Employee.employee_code == employee_code))

        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Employee deleted successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        await db.rollback()
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
