import secrets
from datetime import datetime, timezone
from typing import Any, Type

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.department import CreateDepartment, UpdateDepartment
from app.core.logger import get_logger
from app.models.departments.department import Department
from app.models.departments.department_tr import DepartmentTr
from app.models.departments.department_section import (
    DepartmentObjective,
    DepartmentObjectiveTr,
    DepartmentCoreFunction,
    DepartmentCoreFunctionTr,
)
from app.models.departments.department_director import (
    DepartmentDirector,
    DepartmentDirectorTr,
    DepartmentDirectorWorkingHour,
    DepartmentDirectorWorkingHourTr,
    DepartmentDirectorEducation,
    DepartmentDirectorEducationTr,
)
from app.models.departments.department_personnel import DepartmentWorker, DepartmentWorkerTr
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload

logger = get_logger(__name__)


def _department_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


# ── Section helpers ────────────────────────────────────────────────────────────


async def _create_html_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    department_code: str,
    items: list[Any],
    now: datetime,
    db: AsyncSession,
):
    for index, item in enumerate(items):
        parent = parent_cls(
            department_code=department_code,
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(parent)
        await db.flush()

        db.add(tr_cls(**{parent_id_name: parent.id, "lang_code": "az", "html_content": item.az.html_content, "created_at": now, "updated_at": now}))
        db.add(tr_cls(**{parent_id_name: parent.id, "lang_code": "en", "html_content": item.en.html_content, "created_at": now, "updated_at": now}))


async def _delete_section(parent_cls: Type[Any], department_code: str, db: AsyncSession):
    await db.execute(
        sqlalchemy_delete(parent_cls).where(parent_cls.department_code == department_code)
    )


async def _serialize_html_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    department_code: str,
    lang_code: str,
    db: AsyncSession,
) -> list[dict]:
    parents_q = await db.execute(
        select(parent_cls)
        .where(parent_cls.department_code == department_code)
        .order_by(parent_cls.display_order.asc())
    )
    result = []
    for parent in parents_q.scalars().all():
        tr_q = await db.execute(
            select(tr_cls).where(
                getattr(tr_cls, parent_id_name) == parent.id,
                tr_cls.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()
        result.append({"id": parent.id, "html_content": tr.html_content if tr else None})
    return result


# ── Director helpers ───────────────────────────────────────────────────────────


async def _create_director(department_code: str, data: Any, now: datetime, db: AsyncSession):
    director = DepartmentDirector(
        department_code=department_code,
        first_name=data.first_name,
        last_name=data.last_name,
        father_name=data.father_name,
        room_number=data.room_number,
        profile_image=data.profile_image,
        created_at=now,
        updated_at=now,
    )
    db.add(director)
    await db.flush()

    for lang_code, tr_data in [("az", data.az), ("en", data.en)]:
        if tr_data is None:
            continue
        db.add(DepartmentDirectorTr(
            director_id=director.id,
            lang_code=lang_code,
            scientific_degree=tr_data.scientific_degree,
            scientific_title=tr_data.scientific_title,
            bio=tr_data.bio,
            created_at=now,
            updated_at=now,
        ))

    if data.working_hours:
        for item in data.working_hours:
            wh = DepartmentDirectorWorkingHour(
                director_id=director.id,
                time_range=item.time_range,
                created_at=now,
                updated_at=now,
            )
            db.add(wh)
            await db.flush()
            db.add(DepartmentDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now))
            db.add(DepartmentDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now))

    if data.educations:
        for item in data.educations:
            edu = DepartmentDirectorEducation(
                director_id=director.id,
                start_year=item.start_year,
                end_year=item.end_year,
                created_at=now,
                updated_at=now,
            )
            db.add(edu)
            await db.flush()
            db.add(DepartmentDirectorEducationTr(education_id=edu.id, lang_code="az", degree=item.az.degree, university=item.az.university, created_at=now, updated_at=now))
            db.add(DepartmentDirectorEducationTr(education_id=edu.id, lang_code="en", degree=item.en.degree, university=item.en.university, created_at=now, updated_at=now))

    return director


async def _upsert_director(department_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director_q = await db.execute(
        select(DepartmentDirector).where(DepartmentDirector.department_code == department_code)
    )
    director = director_q.scalar_one_or_none()

    if director_data is None:
        if director:
            await db.execute(sqlalchemy_delete(DepartmentDirector).where(DepartmentDirector.id == director.id))
        return None

    if not director:
        director = DepartmentDirector(department_code=department_code, created_at=now, updated_at=now)
        db.add(director)
        await db.flush()

    data = director_data.dict(exclude_unset=True)
    for field in ["first_name", "last_name", "father_name", "room_number", "profile_image"]:
        if field in data:
            setattr(director, field, data[field])
    director.updated_at = now

    for lang_code, tr_data in [("az", data.get("az")), ("en", data.get("en"))]:
        if tr_data is None:
            continue
        tr_q = await db.execute(
            select(DepartmentDirectorTr).where(
                DepartmentDirectorTr.director_id == director.id,
                DepartmentDirectorTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()
        if tr:
            for field in ["scientific_degree", "scientific_title", "bio"]:
                if field in tr_data:
                    setattr(tr, field, tr_data[field])
            tr.updated_at = now
        else:
            db.add(DepartmentDirectorTr(
                director_id=director.id,
                lang_code=lang_code,
                scientific_degree=tr_data.get("scientific_degree"),
                scientific_title=tr_data.get("scientific_title"),
                bio=tr_data.get("bio"),
                created_at=now,
                updated_at=now,
            ))

    if "working_hours" in data:
        await db.execute(sqlalchemy_delete(DepartmentDirectorWorkingHour).where(DepartmentDirectorWorkingHour.director_id == director.id))
        for item in (data["working_hours"] or []):
            wh = DepartmentDirectorWorkingHour(director_id=director.id, time_range=item.time_range, created_at=now, updated_at=now)
            db.add(wh)
            await db.flush()
            db.add(DepartmentDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now))
            db.add(DepartmentDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now))

    if "educations" in data:
        await db.execute(sqlalchemy_delete(DepartmentDirectorEducation).where(DepartmentDirectorEducation.director_id == director.id))
        for item in (data["educations"] or []):
            edu = DepartmentDirectorEducation(director_id=director.id, start_year=item.start_year, end_year=item.end_year, created_at=now, updated_at=now)
            db.add(edu)
            await db.flush()
            db.add(DepartmentDirectorEducationTr(education_id=edu.id, lang_code="az", degree=item.az.degree, university=item.az.university, created_at=now, updated_at=now))
            db.add(DepartmentDirectorEducationTr(education_id=edu.id, lang_code="en", degree=item.en.degree, university=item.en.university, created_at=now, updated_at=now))

    return director


async def _serialize_director(director: DepartmentDirector, lang_code: str, db: AsyncSession) -> dict | None:
    if not director:
        return None

    tr_q = await db.execute(
        select(DepartmentDirectorTr).where(
            DepartmentDirectorTr.director_id == director.id,
            DepartmentDirectorTr.lang_code == lang_code,
        )
    )
    tr = tr_q.scalar_one_or_none()

    wh_q = await db.execute(select(DepartmentDirectorWorkingHour).where(DepartmentDirectorWorkingHour.director_id == director.id))
    working_hours = []
    for hour in wh_q.scalars().all():
        wh_tr_q = await db.execute(
            select(DepartmentDirectorWorkingHourTr).where(
                DepartmentDirectorWorkingHourTr.working_hour_id == hour.id,
                DepartmentDirectorWorkingHourTr.lang_code == lang_code,
            )
        )
        wh_tr = wh_tr_q.scalar_one_or_none()
        working_hours.append({"day": wh_tr.day if wh_tr else None, "time_range": hour.time_range})

    edu_q = await db.execute(select(DepartmentDirectorEducation).where(DepartmentDirectorEducation.director_id == director.id))
    educations = []
    for edu in edu_q.scalars().all():
        edu_tr_q = await db.execute(
            select(DepartmentDirectorEducationTr).where(
                DepartmentDirectorEducationTr.education_id == edu.id,
                DepartmentDirectorEducationTr.lang_code == lang_code,
            )
        )
        edu_tr = edu_tr_q.scalar_one_or_none()
        educations.append({
            "degree": edu_tr.degree if edu_tr else None,
            "university": edu_tr.university if edu_tr else None,
            "start_year": edu.start_year,
            "end_year": edu.end_year,
        })

    return {
        "id": director.id,
        "first_name": director.first_name,
        "last_name": director.last_name,
        "father_name": director.father_name,
        "room_number": director.room_number,
        "profile_image": director.profile_image,
        "scientific_degree": tr.scientific_degree if tr else None,
        "scientific_title": tr.scientific_title if tr else None,
        "bio": tr.bio if tr else None,
        "working_hours": working_hours,
        "educations": educations,
    }


# ── Worker helpers ─────────────────────────────────────────────────────────────


async def _create_workers(department_code: str, workers: list[Any], now: datetime, db: AsyncSession):
    for item in workers:
        worker = DepartmentWorker(
            department_code=department_code,
            first_name=item.first_name,
            last_name=item.last_name,
            father_name=item.father_name,
            email=item.email,
            phone=item.phone,
            profile_image=item.profile_image,
            created_at=now,
            updated_at=now,
        )
        db.add(worker)
        await db.flush()

        for lang_code, tr_data in [("az", item.az), ("en", item.en)]:
            db.add(DepartmentWorkerTr(
                worker_id=worker.id,
                lang_code=lang_code,
                duty=tr_data.duty,
                scientific_degree=tr_data.scientific_degree,
                scientific_name=tr_data.scientific_name,
                created_at=now,
                updated_at=now,
            ))


async def _serialize_workers(department_code: str, lang_code: str, db: AsyncSession) -> list[dict]:
    workers_q = await db.execute(select(DepartmentWorker).where(DepartmentWorker.department_code == department_code))
    result = []
    for worker in workers_q.scalars().all():
        tr_q = await db.execute(
            select(DepartmentWorkerTr).where(
                DepartmentWorkerTr.worker_id == worker.id,
                DepartmentWorkerTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()
        result.append({
            "id": worker.id,
            "first_name": worker.first_name,
            "last_name": worker.last_name,
            "father_name": worker.father_name,
            "email": worker.email,
            "phone": worker.phone,
            "profile_image": worker.profile_image,
            "duty": tr.duty if tr else None,
            "scientific_degree": tr.scientific_degree if tr else None,
            "scientific_name": tr.scientific_name if tr else None,
        })
    return result


# ── Public service functions ───────────────────────────────────────────────────


async def create_department(request: CreateDepartment, db: AsyncSession):
    try:
        department_code = None
        for _ in range(10):
            candidate = _department_code_generator()
            existing_q = await db.execute(select(Department).where(Department.department_code == candidate))
            if not existing_q.scalar_one_or_none():
                department_code = candidate
                break

        if not department_code:
            return JSONResponse(
                content={"status_code": 500, "message": "Failed to generate unique department code."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        for lang_code, translation in [("az", request.az), ("en", request.en)]:
            dup_q = await db.execute(
                select(DepartmentTr).where(
                    func.lower(DepartmentTr.department_name) == func.lower(translation.department_name),
                    DepartmentTr.lang_code == lang_code,
                )
            )
            if dup_q.scalar_one_or_none():
                return JSONResponse(
                    content={
                        "status_code": 422,
                        "errors": {"department_name": [f"Department name '{translation.department_name}' ({lang_code}) already exists."]},
                    },
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        now = datetime.now(timezone.utc)
        department = Department(department_code=department_code, created_at=now, updated_at=now)
        db.add(department)

        db.add(DepartmentTr(department_code=department_code, lang_code="az", department_name=request.az.department_name, about_html=request.az.about_html, created_at=now, updated_at=now))
        db.add(DepartmentTr(department_code=department_code, lang_code="en", department_name=request.en.department_name, about_html=request.en.about_html, created_at=now, updated_at=now))

        if request.objectives:
            await _create_html_section(DepartmentObjective, DepartmentObjectiveTr, "objective_id", department_code, request.objectives, now, db)

        if request.core_functions:
            await _create_html_section(DepartmentCoreFunction, DepartmentCoreFunctionTr, "core_function_id", department_code, request.core_functions, now, db)

        if request.director:
            await _create_director(department_code, request.director, now, db)

        if request.workers:
            await _create_workers(department_code, request.workers, now, db)

        await db.commit()
        await db.refresh(department)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Department created successfully.",
                "data": {"department_code": department.department_code, "created_at": department.created_at.isoformat()},
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_departments(start: int, end: int, lang: str, db: AsyncSession):
    try:
        total_q = await db.execute(select(func.count()).select_from(Department))
        total = total_q.scalar() or 0

        depts_q = await db.execute(
            select(Department).order_by(Department.id.asc()).offset(start).limit(end - start)
        )
        departments = depts_q.scalars().all()

        if not departments:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        result = []
        for dept in departments:
            tr_q = await db.execute(
                select(DepartmentTr).where(
                    DepartmentTr.department_code == dept.department_code,
                    DepartmentTr.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()

            worker_count_q = await db.execute(
                select(func.count()).select_from(DepartmentWorker).where(DepartmentWorker.department_code == dept.department_code)
            )
            worker_count = worker_count_q.scalar() or 0

            result.append({
                "id": dept.id,
                "department_code": dept.department_code,
                "department_name": tr.department_name if tr else None,
                "worker_count": worker_count,
                "created_at": dept.created_at.isoformat() if dept.created_at else None,
                "updated_at": dept.updated_at.isoformat() if dept.updated_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "Departments fetched successfully.", "departments": result, "total": total},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_department(department_code: str, lang_code: str, db: AsyncSession):
    try:
        dept_q = await db.execute(select(Department).where(Department.department_code == department_code))
        department = dept_q.scalar_one_or_none()

        if not department:
            return JSONResponse(
                content={"status_code": 404, "message": "Department not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(DepartmentTr).where(
                DepartmentTr.department_code == department_code,
                DepartmentTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()

        director_q = await db.execute(select(DepartmentDirector).where(DepartmentDirector.department_code == department_code))
        director = director_q.scalar_one_or_none()

        dept_obj = {
            "id": department.id,
            "department_code": department.department_code,
            "department_name": tr.department_name if tr else None,
            "about_html": tr.about_html if tr else None,
            "objectives": await _serialize_html_section(DepartmentObjective, DepartmentObjectiveTr, "objective_id", department_code, lang_code, db),
            "core_functions": await _serialize_html_section(DepartmentCoreFunction, DepartmentCoreFunctionTr, "core_function_id", department_code, lang_code, db),
            "director": await _serialize_director(director, lang_code, db),
            "workers": await _serialize_workers(department_code, lang_code, db),
            "created_at": department.created_at.isoformat() if department.created_at else None,
            "updated_at": department.updated_at.isoformat() if department.updated_at else None,
        }

        return JSONResponse(
            content={"status_code": 200, "message": "Department fetched successfully.", "department": dept_obj},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_department(department_code: str, request: UpdateDepartment, db: AsyncSession):
    try:
        dept_q = await db.execute(select(Department).where(Department.department_code == department_code))
        department = dept_q.scalar_one_or_none()

        if not department:
            return JSONResponse(
                content={"status_code": 404, "message": "Department not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data = request.dict(exclude_unset=True)
        if not data:
            return JSONResponse(
                content={"status_code": 400, "message": "No fields to update."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.now(timezone.utc)

        async def _upsert_translation(lang: str, translation_data: Any):
            if translation_data is None:
                return
            if translation_data.department_name:
                dup_q = await db.execute(
                    select(DepartmentTr).where(
                        func.lower(DepartmentTr.department_name) == func.lower(translation_data.department_name),
                        DepartmentTr.lang_code == lang,
                        DepartmentTr.department_code != department_code,
                    )
                )
                if dup_q.scalar_one_or_none():
                    raise ValueError(f"Department name '{translation_data.department_name}' ({lang}) already exists.")
            tr_q = await db.execute(
                select(DepartmentTr).where(DepartmentTr.department_code == department_code, DepartmentTr.lang_code == lang)
            )
            tr = tr_q.scalar_one_or_none()
            if tr:
                if translation_data.department_name is not None:
                    tr.department_name = translation_data.department_name
                if translation_data.about_html is not None:
                    tr.about_html = translation_data.about_html
                tr.updated_at = now
            else:
                db.add(DepartmentTr(
                    department_code=department_code,
                    lang_code=lang,
                    department_name=translation_data.department_name or "",
                    about_html=translation_data.about_html,
                    created_at=now,
                    updated_at=now,
                ))

        await _upsert_translation("az", data.get("az"))
        await _upsert_translation("en", data.get("en"))

        if "objectives" in data:
            await _delete_section(DepartmentObjective, department_code, db)
            if data["objectives"]:
                await _create_html_section(DepartmentObjective, DepartmentObjectiveTr, "objective_id", department_code, data["objectives"], now, db)

        if "core_functions" in data:
            await _delete_section(DepartmentCoreFunction, department_code, db)
            if data["core_functions"]:
                await _create_html_section(DepartmentCoreFunction, DepartmentCoreFunctionTr, "core_function_id", department_code, data["core_functions"], now, db)

        if "director" in data:
            await _upsert_director(department_code, data.get("director"), now, db)

        if "workers" in data:
            await db.execute(sqlalchemy_delete(DepartmentWorker).where(DepartmentWorker.department_code == department_code))
            if data["workers"]:
                await _create_workers(department_code, data["workers"], now, db)

        department.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Department updated successfully.",
                "data": {"department_code": department.department_code, "updated_at": department.updated_at.isoformat()},
            },
            status_code=status.HTTP_200_OK,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 422, "errors": {"department_name": [str(e)]}},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_department(department_code: str, db: AsyncSession):
    try:
        dept_q = await db.execute(select(Department).where(Department.department_code == department_code))
        if not dept_q.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Department not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await db.execute(sqlalchemy_delete(Department).where(Department.department_code == department_code))
        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Department deleted successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_director_image(department_code: str, image: UploadFile, db: AsyncSession):
    try:
        director_q = await db.execute(select(DepartmentDirector).where(DepartmentDirector.department_code == department_code))
        director = director_q.scalar_one_or_none()

        if not director:
            return JSONResponse(
                content={"status_code": 404, "message": "Director not found for this department."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = director.profile_image
        new_path = await save_upload(image, "department-directors", ALLOWED_IMAGE_MIMES)

        director.profile_image = new_path
        director.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={"status_code": 200, "message": "Director image uploaded successfully.", "data": {"profile_image": new_path}},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_worker_image(worker_id: int, image: UploadFile, db: AsyncSession):
    try:
        worker_q = await db.execute(select(DepartmentWorker).where(DepartmentWorker.id == worker_id))
        worker = worker_q.scalar_one_or_none()

        if not worker:
            return JSONResponse(
                content={"status_code": 404, "message": "Worker not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = worker.profile_image
        new_path = await save_upload(image, "department-workers", ALLOWED_IMAGE_MIMES)

        worker.profile_image = new_path
        worker.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={"status_code": 200, "message": "Worker image uploaded successfully.", "data": {"profile_image": new_path}},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
