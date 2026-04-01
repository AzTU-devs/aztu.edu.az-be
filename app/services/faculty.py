import secrets
from datetime import datetime, timezone
from typing import Any, Type

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.faculty import CreateFaculty, UpdateFaculty
from app.core.logger import get_logger
from app.core.session import get_db
from app.models.cafedras.cafedras import Cafedra
from app.models.faculties.faculties import Faculty
from app.models.faculties.faculties_tr import FacultyTr
from app.models.faculties.faculty_director import FacultyDirector
from app.models.faculties.faculty_director_relations import (
    FacultyDirectorEducation,
    FacultyDirectorScientificEvent,
    FacultyDirectorWorkingHour,
)
from app.models.faculties.faculty_personnel import (
    FacultyCouncilMember,
    FacultyDeputyDean,
    FacultyWorker,
)
from app.models.faculties.faculty_section import (
    FacultyDuty,
    FacultyDutyTr,
    FacultyLaboratory,
    FacultyLaboratoryTr,
    FacultyObjective,
    FacultyObjectiveTr,
    FacultyPartnerCompany,
    FacultyPartnerCompanyTr,
    FacultyProject,
    FacultyProjectTr,
    FacultyResearchWork,
    FacultyResearchWorkTr,
)
from app.utils.language import get_language

logger = get_logger(__name__)


def faculty_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


async def _create_translated_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    faculty_code: str,
    items: list[Any],
    now: datetime,
    db: AsyncSession,
):
    for index, item in enumerate(items):
        parent = parent_cls(
            faculty_code=faculty_code,
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(parent)
        await db.flush()

        db.add(
            tr_cls(
                **{
                    parent_id_name: parent.id,
                    "lang_code": "az",
                    "title": item.az.title,
                    "description": item.az.description,
                    "created_at": now,
                    "updated_at": now,
                }
            )
        )
        db.add(
            tr_cls(
                **{
                    parent_id_name: parent.id,
                    "lang_code": "en",
                    "title": item.en.title,
                    "description": item.en.description,
                    "created_at": now,
                    "updated_at": now,
                }
            )
        )


async def _serialize_translated_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    faculty_code: str,
    lang_code: str,
    db: AsyncSession,
):
    items = []
    parents_query = await db.execute(
        select(parent_cls).where(parent_cls.faculty_code == faculty_code).order_by(parent_cls.display_order.asc())
    )
    parents = parents_query.scalars().all()
    for parent in parents:
        tr_query = await db.execute(
            select(tr_cls).where(
                getattr(tr_cls, parent_id_name) == parent.id,
                tr_cls.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()
        items.append(
            {
                "id": parent.id,
                "title": tr.title if tr else None,
                "description": tr.description if tr else None,
            }
        )
    return items


async def _create_people(parent_cls: Type[Any], items: list[Any], faculty_code: str, now: datetime, db: AsyncSession):
    for item in items:
        payload = {
            "faculty_code": faculty_code,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "father_name": item.father_name,
            "scientific_name": getattr(item, "scientific_name", None),
            "scientific_degree": getattr(item, "scientific_degree", None),
            "email": getattr(item, "email", None),
            "phone": getattr(item, "phone", None),
            "profile_image": getattr(item, "profile_image", None),
            "duty": getattr(item, "duty", None),
            "created_at": now,
            "updated_at": now,
        }
        allowed = {k: v for k, v in payload.items() if hasattr(parent_cls, k)}
        db.add(parent_cls(**allowed))


async def _create_director(faculty_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director = FacultyDirector(
        faculty_code=faculty_code,
        first_name=director_data.first_name,
        last_name=director_data.last_name,
        father_name=director_data.father_name,
        scientific_degree=director_data.scientific_degree,
        scientific_title=director_data.scientific_title,
        email=director_data.email,
        phone=director_data.phone,
        room_number=director_data.room_number,
        profile_image=director_data.profile_image,
        created_at=now,
        updated_at=now,
    )
    db.add(director)
    await db.flush()

    if director_data.working_hours:
        for item in director_data.working_hours:
            db.add(
                FacultyDirectorWorkingHour(
                    director_id=director.id,
                    day=item.day,
                    time_range=item.time_range,
                    created_at=now,
                    updated_at=now,
                )
            )

    if director_data.scientific_events:
        for item in director_data.scientific_events:
            db.add(
                FacultyDirectorScientificEvent(
                    director_id=director.id,
                    event_title=item.event_title,
                    event_description=item.event_description,
                    created_at=now,
                    updated_at=now,
                )
            )

    if director_data.educations:
        for item in director_data.educations:
            db.add(
                FacultyDirectorEducation(
                    director_id=director.id,
                    degree=item.degree,
                    university=item.university,
                    start_year=item.start_year,
                    end_year=item.end_year,
                    created_at=now,
                    updated_at=now,
                )
            )


async def _upsert_director(faculty_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director_query = await db.execute(
        select(FacultyDirector).where(FacultyDirector.faculty_code == faculty_code)
    )
    director = director_query.scalar_one_or_none()

    if director_data is None:
        if director:
            await db.execute(
                sqlalchemy_delete(FacultyDirector).where(FacultyDirector.id == director.id)
            )
        return None

    if not director:
        director = FacultyDirector(
            faculty_code=faculty_code,
            created_at=now,
            updated_at=now,
        )
        db.add(director)
        await db.flush()

    data = director_data.dict(exclude_unset=True)
    for field in [
        "first_name",
        "last_name",
        "father_name",
        "scientific_degree",
        "scientific_title",
        "bio",
        "email",
        "phone",
        "room_number",
        "profile_image",
    ]:
        if field in data:
            setattr(director, field, data[field])
    director.updated_at = now

    if "working_hours" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorWorkingHour).where(
                FacultyDirectorWorkingHour.director_id == director.id
            )
        )
        if data["working_hours"]:
            for item in data["working_hours"]:
                db.add(
                    FacultyDirectorWorkingHour(
                        director_id=director.id,
                        day=item.day,
                        time_range=item.time_range,
                        created_at=now,
                        updated_at=now,
                    )
                )

    if "scientific_events" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorScientificEvent).where(
                FacultyDirectorScientificEvent.director_id == director.id
            )
        )
        if data["scientific_events"]:
            for item in data["scientific_events"]:
                db.add(
                    FacultyDirectorScientificEvent(
                        director_id=director.id,
                        event_title=item.event_title,
                        event_description=item.event_description,
                        created_at=now,
                        updated_at=now,
                    )
                )

    if "educations" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorEducation).where(
                FacultyDirectorEducation.director_id == director.id
            )
        )
        if data["educations"]:
            for item in data["educations"]:
                db.add(
                    FacultyDirectorEducation(
                        director_id=director.id,
                        degree=item.degree,
                        university=item.university,
                        start_year=item.start_year,
                        end_year=item.end_year,
                        created_at=now,
                        updated_at=now,
                    )
                )

    return director


async def _delete_section(parent_cls: Type[Any], faculty_code: str, db: AsyncSession):
    await db.execute(
        sqlalchemy_delete(parent_cls).where(parent_cls.faculty_code == faculty_code)
    )


async def _fetch_people(parent_cls: Type[Any], faculty_code: str, db: AsyncSession):
    query = await db.execute(
        select(parent_cls).where(parent_cls.faculty_code == faculty_code)
    )
    return query.scalars().all()


async def _serialize_director(director: FacultyDirector, db: AsyncSession):
    if not director:
        return None

    working_hours_query = await db.execute(
        select(FacultyDirectorWorkingHour).where(
            FacultyDirectorWorkingHour.director_id == director.id
        )
    )
    scientific_events_query = await db.execute(
        select(FacultyDirectorScientificEvent).where(
            FacultyDirectorScientificEvent.director_id == director.id
        )
    )
    educations_query = await db.execute(
        select(FacultyDirectorEducation).where(
            FacultyDirectorEducation.director_id == director.id
        )
    )

    return {
        "first_name": director.first_name,
        "last_name": director.last_name,
        "father_name": director.father_name,
        "scientific_degree": director.scientific_degree,
        "scientific_title": director.scientific_title,
        "email": director.email,
        "phone": director.phone,
        "room_number": director.room_number,
        "profile_image": director.profile_image,
        "working_hours": [
            {
                "day": hour.day,
                "time_range": hour.time_range,
            }
            for hour in working_hours_query.scalars().all()
        ],
        "scientific_events": [
            {
                "event_title": event.event_title,
                "event_description": event.event_description,
            }
            for event in scientific_events_query.scalars().all()
        ],
        "educations": [
            {
                "degree": education.degree,
                "university": education.university,
                "start_year": education.start_year,
                "end_year": education.end_year,
            }
            for education in educations_query.scalars().all()
        ],
    }


async def create_faculty(
    request: CreateFaculty,
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_code = None
        for _ in range(10):
            candidate = faculty_code_generator()
            existing_query = await db.execute(
                select(Faculty).where(Faculty.faculty_code == candidate)
            )
            if not existing_query.scalar_one_or_none():
                faculty_code = candidate
                break

        if not faculty_code:
            return JSONResponse(
                content={
                    "status_code": 500,
                    "message": "Failed to generate unique faculty code.",
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        for lang_code, translation in [("az", request.az), ("en", request.en)]:
            dup_q = await db.execute(
                select(FacultyTr).where(
                    func.lower(FacultyTr.faculty_name) == func.lower(translation.title),
                    FacultyTr.lang_code == lang_code,
                )
            )
            if dup_q.scalar_one_or_none():
                return JSONResponse(
                    content={
                        "status_code": 422,
                        "errors": {
                            "title": [
                                f"Faculty title '{translation.title}' ({lang_code}) already exists (case-insensitive)."
                            ]
                        },
                    },
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        now = datetime.now(timezone.utc)
        faculty = Faculty(
            faculty_code=faculty_code,
            created_at=now,
        )
        db.add(faculty)

        db.add(
            FacultyTr(
                faculty_code=faculty_code,
                lang_code="az",
                faculty_name=request.az.title,
                about_text=request.az.html_content,
                created_at=now,
            )
        )
        db.add(
            FacultyTr(
                faculty_code=faculty_code,
                lang_code="en",
                faculty_name=request.en.title,
                about_text=request.en.html_content,
                created_at=now,
            )
        )

        if request.director:
            await _create_director(faculty_code, request.director, now, db)

        if request.laboratories:
            await _create_translated_section(
                FacultyLaboratory,
                FacultyLaboratoryTr,
                "laboratory_id",
                faculty_code,
                request.laboratories,
                now,
                db,
            )

        if request.research_works:
            await _create_translated_section(
                FacultyResearchWork,
                FacultyResearchWorkTr,
                "research_work_id",
                faculty_code,
                request.research_works,
                now,
                db,
            )

        if request.partner_companies:
            await _create_translated_section(
                FacultyPartnerCompany,
                FacultyPartnerCompanyTr,
                "partner_company_id",
                faculty_code,
                request.partner_companies,
                now,
                db,
            )

        if request.objectives:
            await _create_translated_section(
                FacultyObjective,
                FacultyObjectiveTr,
                "objective_id",
                faculty_code,
                request.objectives,
                now,
                db,
            )

        if request.duties:
            await _create_translated_section(
                FacultyDuty,
                FacultyDutyTr,
                "duty_id",
                faculty_code,
                request.duties,
                now,
                db,
            )

        if request.projects:
            await _create_translated_section(
                FacultyProject,
                FacultyProjectTr,
                "project_id",
                faculty_code,
                request.projects,
                now,
                db,
            )

        if request.deputy_deans:
            await _create_people(FacultyDeputyDean, request.deputy_deans, faculty_code, now, db)

        if request.scientific_council:
            await _create_people(FacultyCouncilMember, request.scientific_council, faculty_code, now, db)

        if request.workers:
            await _create_people(FacultyWorker, request.workers, faculty_code, now, db)

        await db.commit()
        await db.refresh(faculty)

        return JSONResponse(
            content={
                "status_code": 201,
                "data": {
                    "faculty_code": faculty.faculty_code,
                    "created_at": faculty.created_at.isoformat()
                    if faculty.created_at
                    else None,
                },
                "message": "Faculty created successfully.",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={
                "status_code": 500,
                "error": "Internal server error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_faculties(
    start: int = 0,
    end: int = 10,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Faculty))
        total = total_query.scalar() or 0

        faculty_query = await db.execute(
            select(Faculty)
            .order_by(Faculty.id.asc())
            .offset(start)
            .limit(end - start)
        )
        faculties = faculty_query.scalars().all()

        if not faculties:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        faculties_arr = []
        for faculty in faculties:
            tr_query = await db.execute(
                select(FacultyTr).where(
                    FacultyTr.faculty_code == faculty.faculty_code,
                    FacultyTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()

            cafedra_count_query = await db.execute(
                select(func.count()).select_from(Cafedra).where(
                    Cafedra.faculty_code == faculty.faculty_code
                )
            )
            cafedra_count = cafedra_count_query.scalar() or 0

            deputy_count_query = await db.execute(
                select(func.count()).select_from(FacultyDeputyDean).where(
                    FacultyDeputyDean.faculty_code == faculty.faculty_code
                )
            )
            deputy_count = deputy_count_query.scalar() or 0

            faculties_arr.append(
                {
                    "id": faculty.id,
                    "faculty_code": faculty.faculty_code,
                    "title": tr.faculty_name if tr else None,
                    "cafedra_count": cafedra_count,
                    "deputy_dean_count": deputy_count,
                    "created_at": faculty.created_at.isoformat()
                    if faculty.created_at
                    else None,
                    "updated_at": faculty.updated_at.isoformat()
                    if faculty.updated_at
                    else None,
                }
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Faculties fetched successfully.",
                "faculties": faculties_arr,
                "total": total,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_faculty(
    faculty_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        faculty = faculty_query.scalar_one_or_none()

        if not faculty:
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_query = await db.execute(
            select(FacultyTr).where(
                FacultyTr.faculty_code == faculty.faculty_code,
                FacultyTr.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()

        director_query = await db.execute(
            select(FacultyDirector).where(FacultyDirector.faculty_code == faculty_code)
        )
        director = director_query.scalar_one_or_none()

        faculty_obj = {
            "id": faculty.id,
            "faculty_code": faculty.faculty_code,
            "title": tr.faculty_name if tr else None,
            "html_content": tr.about_text if tr else None,
            "director": await _serialize_director(director, db) if director else None,
            "laboratories": await _serialize_translated_section(
                FacultyLaboratory,
                FacultyLaboratoryTr,
                "laboratory_id",
                faculty_code,
                lang_code,
                db,
            ),
            "research_works": await _serialize_translated_section(
                FacultyResearchWork,
                FacultyResearchWorkTr,
                "research_work_id",
                faculty_code,
                lang_code,
                db,
            ),
            "partner_companies": await _serialize_translated_section(
                FacultyPartnerCompany,
                FacultyPartnerCompanyTr,
                "partner_company_id",
                faculty_code,
                lang_code,
                db,
            ),
            "objectives": await _serialize_translated_section(
                FacultyObjective,
                FacultyObjectiveTr,
                "objective_id",
                faculty_code,
                lang_code,
                db,
            ),
            "duties": await _serialize_translated_section(
                FacultyDuty,
                FacultyDutyTr,
                "duty_id",
                faculty_code,
                lang_code,
                db,
            ),
            "projects": await _serialize_translated_section(
                FacultyProject,
                FacultyProjectTr,
                "project_id",
                faculty_code,
                lang_code,
                db,
            ),
            "deputy_deans": [
                {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "father_name": person.father_name,
                    "scientific_name": person.scientific_name,
                    "scientific_degree": person.scientific_degree,
                    "email": person.email,
                    "phone": person.phone,
                    "duty": person.duty,
                    "profile_image": person.profile_image,
                }
                for person in (await _fetch_people(FacultyDeputyDean, faculty_code, db))
            ],
            "scientific_council": [
                {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "father_name": person.father_name,
                    "duty": person.duty,
                }
                for person in (await _fetch_people(FacultyCouncilMember, faculty_code, db))
            ],
            "workers": [
                {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "father_name": person.father_name,
                    "duty": person.duty,
                    "scientific_name": person.scientific_name,
                    "scientific_degree": person.scientific_degree,
                    "email": person.email,
                }
                for person in (await _fetch_people(FacultyWorker, faculty_code, db))
            ],
            "created_at": faculty.created_at.isoformat() if faculty.created_at else None,
            "updated_at": faculty.updated_at.isoformat() if faculty.updated_at else None,
        }

        return JSONResponse(
            content={"status_code": 200, "message": "Faculty details fetched successfully.", "faculty": faculty_obj},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_faculty(
    faculty_code: str,
    request: UpdateFaculty,
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        faculty = faculty_query.scalar_one_or_none()

        if not faculty:
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        request_data = request.dict(exclude_unset=True)
        if not request_data:
            return JSONResponse(
                content={"status_code": 400, "message": "No fields to update."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.now(timezone.utc)

        async def ensure_translation(lang: str, translation_data: Any):
            if translation_data is None:
                return
            if translation_data.title:
                dup_q = await db.execute(
                    select(FacultyTr).where(
                        func.lower(FacultyTr.faculty_name) == func.lower(translation_data.title),
                        FacultyTr.lang_code == lang,
                        FacultyTr.faculty_code != faculty_code,
                    )
                )
                if dup_q.scalar_one_or_none():
                    raise ValueError(
                        f"Faculty title '{translation_data.title}' ({lang}) already exists (case-insensitive)."
                    )
            tr_query = await db.execute(
                select(FacultyTr).where(
                    FacultyTr.faculty_code == faculty_code,
                    FacultyTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()
            if tr:
                if translation_data.title is not None:
                    tr.faculty_name = translation_data.title
                if translation_data.html_content is not None:
                    tr.about_text = translation_data.html_content
                tr.updated_at = now
            else:
                db.add(
                    FacultyTr(
                        faculty_code=faculty_code,
                        lang_code=lang,
                        faculty_name=translation_data.title or "",
                        about_text=translation_data.html_content,
                        created_at=now,
                    )
                )

        await ensure_translation("az", request_data.get("az"))
        await ensure_translation("en", request_data.get("en"))

        if "director" in request_data:
            await _upsert_director(faculty_code, request_data.get("director"), now, db)

        if "laboratories" in request_data:
            await _delete_section(FacultyLaboratory, faculty_code, db)
            if request_data["laboratories"]:
                await _create_translated_section(
                    FacultyLaboratory,
                    FacultyLaboratoryTr,
                    "laboratory_id",
                    faculty_code,
                    request_data["laboratories"],
                    now,
                    db,
                )

        if "research_works" in request_data:
            await _delete_section(FacultyResearchWork, faculty_code, db)
            if request_data["research_works"]:
                await _create_translated_section(
                    FacultyResearchWork,
                    FacultyResearchWorkTr,
                    "research_work_id",
                    faculty_code,
                    request_data["research_works"],
                    now,
                    db,
                )

        if "partner_companies" in request_data:
            await _delete_section(FacultyPartnerCompany, faculty_code, db)
            if request_data["partner_companies"]:
                await _create_translated_section(
                    FacultyPartnerCompany,
                    FacultyPartnerCompanyTr,
                    "partner_company_id",
                    faculty_code,
                    request_data["partner_companies"],
                    now,
                    db,
                )

        if "objectives" in request_data:
            await _delete_section(FacultyObjective, faculty_code, db)
            if request_data["objectives"]:
                await _create_translated_section(
                    FacultyObjective,
                    FacultyObjectiveTr,
                    "objective_id",
                    faculty_code,
                    request_data["objectives"],
                    now,
                    db,
                )

        if "duties" in request_data:
            await _delete_section(FacultyDuty, faculty_code, db)
            if request_data["duties"]:
                await _create_translated_section(
                    FacultyDuty,
                    FacultyDutyTr,
                    "duty_id",
                    faculty_code,
                    request_data["duties"],
                    now,
                    db,
                )

        if "projects" in request_data:
            await _delete_section(FacultyProject, faculty_code, db)
            if request_data["projects"]:
                await _create_translated_section(
                    FacultyProject,
                    FacultyProjectTr,
                    "project_id",
                    faculty_code,
                    request_data["projects"],
                    now,
                    db,
                )

        if "deputy_deans" in request_data:
            await _delete_section(FacultyDeputyDean, faculty_code, db)
            if request_data["deputy_deans"]:
                await _create_people(FacultyDeputyDean, request_data["deputy_deans"], faculty_code, now, db)

        if "scientific_council" in request_data:
            await _delete_section(FacultyCouncilMember, faculty_code, db)
            if request_data["scientific_council"]:
                await _create_people(
                    FacultyCouncilMember, request_data["scientific_council"], faculty_code, now, db
                )

        if "workers" in request_data:
            await _delete_section(FacultyWorker, faculty_code, db)
            if request_data["workers"]:
                await _create_people(FacultyWorker, request_data["workers"], faculty_code, now, db)

        faculty.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Faculty updated successfully.",
                "data": {"faculty_code": faculty.faculty_code, "updated_at": faculty.updated_at.isoformat() if faculty.updated_at else None},
            },
            status_code=status.HTTP_200_OK,
        )

    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 422, "errors": {"title": [str(e)]}},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_faculty(
    faculty_code: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        faculty = faculty_query.scalar_one_or_none()

        if not faculty:
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await db.execute(
            sqlalchemy_delete(FacultyTr).where(FacultyTr.faculty_code == faculty_code)
        )
        await db.execute(
            sqlalchemy_delete(Faculty).where(Faculty.faculty_code == faculty_code)
        )

        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Faculty deleted successfully."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
