import secrets
from datetime import datetime, timezone
from typing import Any, Type

from fastapi import Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.faculty import CreateFaculty, UpdateFaculty, CreateDirectionOfAction, UpdateDirectionOfAction, Worker
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload
from app.core.logger import get_logger
from app.core.session import get_db
from app.models.cafedras.cafedras import Cafedra
from app.models.faculties.faculties import Faculty
from app.models.faculties.faculties_tr import FacultyTr
from app.models.faculties.faculty_director import FacultyDirector, FacultyDirectorTr
from app.models.faculties.faculty_director_relations import (
    FacultyDirectorEducation,
    FacultyDirectorEducationTr,
    FacultyDirectorScientificEvent,
    FacultyDirectorScientificEventTr,
    FacultyDirectorWorkingHour,
    FacultyDirectorWorkingHourTr,
)
from app.models.faculties.faculty_personnel import (
    FacultyCouncilMember,
    FacultyCouncilMemberTr,
    FacultyDeputyDean,
    FacultyDeputyDeanTr,
    FacultyWorker,
    FacultyWorkerTr,
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
    FacultyDirectionOfAction,
    FacultyDirectionOfActionTr,
)
from app.utils.language import get_language, get_optional_language

logger = get_logger(__name__)


def validate_sdgs(sdgs: list[int] | None) -> list[int]:
    if not sdgs:
        return []
    valid_sdgs = [i for i in sdgs if 1 <= i <= 17]
    return list(set(valid_sdgs))


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
    lang_code: str | None,
    db: AsyncSession,
):
    items = []
    parents_query = await db.execute(
        select(parent_cls).where(parent_cls.faculty_code == faculty_code).order_by(parent_cls.display_order.asc())
    )
    parents = parents_query.scalars().all()
    for parent in parents:
        if lang_code:
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
        else:
            # Bilingual
            item_data = {"id": parent.id}
            for lc in ["az", "en"]:
                tr_query = await db.execute(
                    select(tr_cls).where(
                        getattr(tr_cls, parent_id_name) == parent.id,
                        tr_cls.lang_code == lc,
                    )
                )
                tr = tr_query.scalar_one_or_none()
                item_data[lc] = {
                    "title": tr.title if tr else None,
                    "description": tr.description if tr else None,
                }
            items.append(item_data)
    return items


async def _create_person_translations(
    tr_cls: Type[Any],
    person_id_field: str,
    person_id: int,
    az_data: Any,
    en_data: Any,
    now: datetime,
    db: AsyncSession,
):
    for lang_code, data in [("az", az_data), ("en", en_data)]:
        if data is None:
            continue
        fields = {person_id_field: person_id, "lang_code": lang_code, "created_at": now, "updated_at": now}
        for attr in ["scientific_name", "scientific_degree", "duty"]:
            if hasattr(tr_cls, attr):
                fields[attr] = getattr(data, attr, None)
        db.add(tr_cls(**fields))


async def _create_people(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    person_id_field: str,
    items: list[Any],
    faculty_code: str,
    now: datetime,
    db: AsyncSession,
):
    for item in items:
        payload = {
            "faculty_code": faculty_code,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "father_name": item.father_name,
            "email": getattr(item, "email", None),
            "phone": getattr(item, "phone", None),
            "profile_image": getattr(item, "profile_image", None),
            "created_at": now,
            "updated_at": now,
        }
        allowed = {k: v for k, v in payload.items() if hasattr(parent_cls, k)}
        person = parent_cls(**allowed)
        db.add(person)
        await db.flush()

        await _create_person_translations(
            tr_cls,
            person_id_field,
            person.id,
            getattr(item, "az", None),
            getattr(item, "en", None),
            now,
            db,
        )


async def _create_director(faculty_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director = FacultyDirector(
        faculty_code=faculty_code,
        first_name=director_data.first_name,
        last_name=director_data.last_name,
        father_name=director_data.father_name,
        email=director_data.email,
        phone=director_data.phone,
        room_number=director_data.room_number,
        profile_image=director_data.profile_image,
        created_at=now,
        updated_at=now,
    )
    db.add(director)
    await db.flush()

    for lang_code, tr_data in [("az", director_data.az), ("en", director_data.en)]:
        if tr_data is None:
            continue
        db.add(FacultyDirectorTr(
            director_id=director.id,
            lang_code=lang_code,
            scientific_degree=tr_data.scientific_degree,
            scientific_title=tr_data.scientific_title,
            bio=tr_data.bio,
            created_at=now,
            updated_at=now,
        ))

    if director_data.working_hours:
        for item in director_data.working_hours:
            wh = FacultyDirectorWorkingHour(
                director_id=director.id,
                time_range=item.time_range,
                created_at=now,
                updated_at=now,
            )
            db.add(wh)
            await db.flush()
            db.add(FacultyDirectorWorkingHourTr(
                working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now,
            ))
            db.add(FacultyDirectorWorkingHourTr(
                working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now,
            ))

    if director_data.scientific_events:
        for item in director_data.scientific_events:
            event = FacultyDirectorScientificEvent(
                director_id=director.id,
                created_at=now,
                updated_at=now,
            )
            db.add(event)
            await db.flush()
            db.add(FacultyDirectorScientificEventTr(
                scientific_event_id=event.id,
                lang_code="az",
                event_title=item.az.event_title,
                event_description=item.az.event_description,
                created_at=now,
                updated_at=now,
            ))
            db.add(FacultyDirectorScientificEventTr(
                scientific_event_id=event.id,
                lang_code="en",
                event_title=item.en.event_title,
                event_description=item.en.event_description,
                created_at=now,
                updated_at=now,
            ))

    if director_data.educations:
        for item in director_data.educations:
            edu = FacultyDirectorEducation(
                director_id=director.id,
                start_year=item.start_year,
                end_year=item.end_year,
                created_at=now,
                updated_at=now,
            )
            db.add(edu)
            await db.flush()
            db.add(FacultyDirectorEducationTr(
                education_id=edu.id,
                lang_code="az",
                degree=item.az.degree,
                university=item.az.university,
                created_at=now,
                updated_at=now,
            ))
            db.add(FacultyDirectorEducationTr(
                education_id=edu.id,
                lang_code="en",
                degree=item.en.degree,
                university=item.en.university,
                created_at=now,
                updated_at=now,
            ))


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
    for field in ["first_name", "last_name", "father_name", "email", "phone", "room_number", "profile_image"]:
        if field in data:
            setattr(director, field, data[field])
    director.updated_at = now

    for lang_code, tr_data in [("az", data.get("az")), ("en", data.get("en"))]:
        if tr_data is None:
            continue
        tr_query = await db.execute(
            select(FacultyDirectorTr).where(
                FacultyDirectorTr.director_id == director.id,
                FacultyDirectorTr.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()
        if tr:
            for field in ["scientific_degree", "scientific_title", "bio", "scientific_research_fields"]:
                if field in tr_data:
                    setattr(tr, field, tr_data[field])
            tr.updated_at = now
        else:
            db.add(FacultyDirectorTr(
                director_id=director.id,
                lang_code=lang_code,
                scientific_degree=tr_data.get("scientific_degree"),
                scientific_title=tr_data.get("scientific_title"),
                bio=tr_data.get("bio"),
                scientific_research_fields=tr_data.get("scientific_research_fields") or [],
                created_at=now,
                updated_at=now,
            ))

    if "working_hours" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorWorkingHour).where(
                FacultyDirectorWorkingHour.director_id == director.id
            )
        )
        if data["working_hours"]:
            for item in data["working_hours"]:
                wh = FacultyDirectorWorkingHour(
                    director_id=director.id,
                    time_range=item.time_range,
                    created_at=now,
                    updated_at=now,
                )
                db.add(wh)
                await db.flush()
                db.add(FacultyDirectorWorkingHourTr(
                    working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now,
                ))
                db.add(FacultyDirectorWorkingHourTr(
                    working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now,
                ))

    if "scientific_events" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorScientificEvent).where(
                FacultyDirectorScientificEvent.director_id == director.id
            )
        )
        if data["scientific_events"]:
            for item in data["scientific_events"]:
                event = FacultyDirectorScientificEvent(
                    director_id=director.id,
                    created_at=now,
                    updated_at=now,
                )
                db.add(event)
                await db.flush()
                db.add(FacultyDirectorScientificEventTr(
                    scientific_event_id=event.id,
                    lang_code="az",
                    event_title=item.az.event_title,
                    event_description=item.az.event_description,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(FacultyDirectorScientificEventTr(
                    scientific_event_id=event.id,
                    lang_code="en",
                    event_title=item.en.event_title,
                    event_description=item.en.event_description,
                    created_at=now,
                    updated_at=now,
                ))

    if "educations" in data:
        await db.execute(
            sqlalchemy_delete(FacultyDirectorEducation).where(
                FacultyDirectorEducation.director_id == director.id
            )
        )
        if data["educations"]:
            for item in data["educations"]:
                edu = FacultyDirectorEducation(
                    director_id=director.id,
                    start_year=item.start_year,
                    end_year=item.end_year,
                    created_at=now,
                    updated_at=now,
                )
                db.add(edu)
                await db.flush()
                db.add(FacultyDirectorEducationTr(
                    education_id=edu.id,
                    lang_code="az",
                    degree=item.az.degree,
                    university=item.az.university,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(FacultyDirectorEducationTr(
                    education_id=edu.id,
                    lang_code="en",
                    degree=item.en.degree,
                    university=item.en.university,
                    created_at=now,
                    updated_at=now,
                ))

    return director


async def _delete_section(parent_cls: Type[Any], faculty_code: str, db: AsyncSession):
    await db.execute(
        sqlalchemy_delete(parent_cls).where(parent_cls.faculty_code == faculty_code)
    )


async def _fetch_people_with_tr(parent_cls: Type[Any], tr_cls: Type[Any], person_id_field: str, faculty_code: str, lang_code: str | None, db: AsyncSession):
    query = await db.execute(
        select(parent_cls).where(parent_cls.faculty_code == faculty_code)
    )
    people = query.scalars().all()
    result = []
    for person in people:
        if lang_code:
            tr_query = await db.execute(
                select(tr_cls).where(
                    getattr(tr_cls, person_id_field) == person.id,
                    tr_cls.lang_code == lang_code,
                )
            )
            tr = tr_query.scalar_one_or_none()
            result.append((person, tr))
        else:
            # Bilingual
            tr_data = {}
            for lc in ["az", "en"]:
                tr_query = await db.execute(
                    select(tr_cls).where(
                        getattr(tr_cls, person_id_field) == person.id,
                        tr_cls.lang_code == lc,
                    )
                )
                tr_data[lc] = tr_query.scalar_one_or_none()
            result.append((person, tr_data))
    return result


async def _serialize_director(director: FacultyDirector, lang_code: str | None, db: AsyncSession):
    if not director:
        return None

    if lang_code:
        tr_query = await db.execute(
            select(FacultyDirectorTr).where(
                FacultyDirectorTr.director_id == director.id,
                FacultyDirectorTr.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()
    else:
        tr = None

    tr_bilingual = {}
    if not lang_code:
        for lc in ["az", "en"]:
            lc_query = await db.execute(
                select(FacultyDirectorTr).where(
                    FacultyDirectorTr.director_id == director.id,
                    FacultyDirectorTr.lang_code == lc,
                )
            )
            tr_bilingual[lc] = lc_query.scalar_one_or_none()

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

    working_hours = []
    for hour in working_hours_query.scalars().all():
        if lang_code:
            wh_tr_q = await db.execute(
                select(FacultyDirectorWorkingHourTr).where(
                    FacultyDirectorWorkingHourTr.working_hour_id == hour.id,
                    FacultyDirectorWorkingHourTr.lang_code == lang_code,
                )
            )
            wh_tr = wh_tr_q.scalar_one_or_none()
            working_hours.append({
                "day": wh_tr.day if wh_tr else None,
                "time_range": hour.time_range,
            })
        else:
            wh_item = {"time_range": hour.time_range}
            for lc in ["az", "en"]:
                wh_tr_q = await db.execute(
                    select(FacultyDirectorWorkingHourTr).where(
                        FacultyDirectorWorkingHourTr.working_hour_id == hour.id,
                        FacultyDirectorWorkingHourTr.lang_code == lc,
                    )
                )
                wh_tr = wh_tr_q.scalar_one_or_none()
                wh_item[lc] = {"day": wh_tr.day if wh_tr else None}
            working_hours.append(wh_item)

    scientific_events = []
    for event in scientific_events_query.scalars().all():
        if lang_code:
            ev_tr_q = await db.execute(
                select(FacultyDirectorScientificEventTr).where(
                    FacultyDirectorScientificEventTr.scientific_event_id == event.id,
                    FacultyDirectorScientificEventTr.lang_code == lang_code,
                )
            )
            ev_tr = ev_tr_q.scalar_one_or_none()
            scientific_events.append({
                "event_title": ev_tr.event_title if ev_tr else None,
                "event_description": ev_tr.event_description if ev_tr else None,
            })
        else:
            ev_item = {}
            for lc in ["az", "en"]:
                ev_tr_q = await db.execute(
                    select(FacultyDirectorScientificEventTr).where(
                        FacultyDirectorScientificEventTr.scientific_event_id == event.id,
                        FacultyDirectorScientificEventTr.lang_code == lc,
                    )
                )
                ev_tr = ev_tr_q.scalar_one_or_none()
                ev_item[lc] = {
                    "event_title": ev_tr.event_title if ev_tr else None,
                    "event_description": ev_tr.event_description if ev_tr else None,
                }
            scientific_events.append(ev_item)

    educations = []
    for edu in educations_query.scalars().all():
        if lang_code:
            edu_tr_q = await db.execute(
                select(FacultyDirectorEducationTr).where(
                    FacultyDirectorEducationTr.education_id == edu.id,
                    FacultyDirectorEducationTr.lang_code == lang_code,
                )
            )
            edu_tr = edu_tr_q.scalar_one_or_none()
            educations.append({
                "degree": edu_tr.degree if edu_tr else None,
                "university": edu_tr.university if edu_tr else None,
                "start_year": edu.start_year,
                "end_year": edu.end_year,
            })
        else:
            edu_item = {"start_year": edu.start_year, "end_year": edu.end_year}
            for lc in ["az", "en"]:
                edu_tr_q = await db.execute(
                    select(FacultyDirectorEducationTr).where(
                        FacultyDirectorEducationTr.education_id == edu.id,
                        FacultyDirectorEducationTr.lang_code == lc,
                    )
                )
                edu_tr = edu_tr_q.scalar_one_or_none()
                edu_item[lc] = {
                    "degree": edu_tr.degree if edu_tr else None,
                    "university": edu_tr.university if edu_tr else None,
                }
            educations.append(edu_item)

    result = {
        "first_name": director.first_name,
        "last_name": director.last_name,
        "father_name": director.father_name,
        "email": director.email,
        "phone": director.phone,
        "room_number": director.room_number,
        "profile_image": director.profile_image,
        "working_hours": working_hours,
        "scientific_events": scientific_events,
        "educations": educations,
    }

    if lang_code:
        result["scientific_degree"] = tr.scientific_degree if tr else None
        result["scientific_title"] = tr.scientific_title if tr else None
        result["bio"] = tr.bio if tr else None
        result["scientific_research_fields"] = tr.scientific_research_fields if tr else []
    else:
        for lc in ["az", "en"]:
            lc_tr = tr_bilingual.get(lc)
            result[lc] = {
                "scientific_degree": lc_tr.scientific_degree if lc_tr else None,
                "scientific_title": lc_tr.scientific_title if lc_tr else None,
                "bio": lc_tr.bio if lc_tr else None,
                "scientific_research_fields": lc_tr.scientific_research_fields if lc_tr else [],
            }

    return result


async def create_faculty(
    request: CreateFaculty,
    db: AsyncSession = Depends(get_db),
):
    try:
        logger.debug("Creating faculty with payload: %s", request.dict())
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
                logger.warning("Duplicate faculty title found: %s (%s)", translation.title, lang_code)
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
            bachelor_programs_count=request.bachelor_programs_count or 0,
            master_programs_count=request.master_programs_count or 0,
            phd_programs_count=request.phd_programs_count or 0,
            international_collaborations_count=request.international_collaborations_count or 0,
            laboratories_count=request.laboratories_count or 0,
            projects_patents_count=request.projects_patents_count or 0,
            industrial_collaborations_count=request.industrial_collaborations_count or 0,
            sdgs=validate_sdgs(request.sdgs),
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
                FacultyLaboratory, FacultyLaboratoryTr, "laboratory_id", faculty_code, request.laboratories, now, db,
            )

        if request.research_works:
            await _create_translated_section(
                FacultyResearchWork, FacultyResearchWorkTr, "research_work_id", faculty_code, request.research_works, now, db,
            )

        if request.partner_companies:
            await _create_translated_section(
                FacultyPartnerCompany, FacultyPartnerCompanyTr, "partner_company_id", faculty_code, request.partner_companies, now, db,
            )

        if request.objectives:
            await _create_translated_section(
                FacultyObjective, FacultyObjectiveTr, "objective_id", faculty_code, request.objectives, now, db,
            )

        if request.duties:
            await _create_translated_section(
                FacultyDuty, FacultyDutyTr, "duty_id", faculty_code, request.duties, now, db,
            )

        if request.projects:
            await _create_translated_section(
                FacultyProject, FacultyProjectTr, "project_id", faculty_code, request.projects, now, db,
            )

        if request.directions_of_action:
            await _create_translated_section(
                FacultyDirectionOfAction, FacultyDirectionOfActionTr, "direction_of_action_id", faculty_code, request.directions_of_action, now, db,
            )

        if request.deputy_deans:
            await _create_people(FacultyDeputyDean, FacultyDeputyDeanTr, "deputy_dean_id", request.deputy_deans, faculty_code, now, db)

        if request.scientific_council:
            await _create_people(FacultyCouncilMember, FacultyCouncilMemberTr, "council_member_id", request.scientific_council, faculty_code, now, db)

        if request.workers:
            await _create_people(FacultyWorker, FacultyWorkerTr, "worker_id", request.workers, faculty_code, now, db)

        await db.commit()
        await db.refresh(faculty)

        return JSONResponse(
            content={
                "status_code": 201,
                "data": {
                    "faculty_code": faculty.faculty_code,
                    "created_at": faculty.created_at.isoformat() if faculty.created_at else None,
                },
                "message": "Faculty created successfully.",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
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
                    "created_at": faculty.created_at.isoformat() if faculty.created_at else None,
                    "updated_at": faculty.updated_at.isoformat() if faculty.updated_at else None,
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


def _serialize_people(people_with_tr: list, lang_code: str | None, has_profile_image: bool = False) -> list:
    result = []
    for person, tr_data in people_with_tr:
        item = {
            "id": person.id,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "father_name": person.father_name,
            "email": person.email,
            "phone": person.phone,
        }
        if has_profile_image:
            item["profile_image"] = person.profile_image

        if lang_code:
            item["scientific_name"] = tr_data.scientific_name if tr_data else None
            item["scientific_degree"] = tr_data.scientific_degree if tr_data else None
            item["duty"] = tr_data.duty if tr_data else None
        else:
            for lc in ["az", "en"]:
                lc_tr = tr_data.get(lc) if isinstance(tr_data, dict) else None
                item[lc] = {
                    "scientific_name": lc_tr.scientific_name if lc_tr else None,
                    "scientific_degree": lc_tr.scientific_degree if lc_tr else None,
                    "duty": lc_tr.duty if lc_tr else None,
                }
        result.append(item)
    return result


async def get_faculty(
    faculty_code: str,
    lang_code: str = Depends(get_optional_language),
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

        if lang_code:
            tr_query = await db.execute(
                select(FacultyTr).where(
                    FacultyTr.faculty_code == faculty.faculty_code,
                    FacultyTr.lang_code == lang_code,
                )
            )
            tr = tr_query.scalar_one_or_none()
            tr_bilingual = None
        else:
            tr = None
            tr_bilingual = {}
            for lc in ["az", "en"]:
                lc_query = await db.execute(
                    select(FacultyTr).where(
                        FacultyTr.faculty_code == faculty.faculty_code,
                        FacultyTr.lang_code == lc,
                    )
                )
                tr_bilingual[lc] = lc_query.scalar_one_or_none()

        director_query = await db.execute(
            select(FacultyDirector).where(FacultyDirector.faculty_code == faculty_code)
        )
        director = director_query.scalar_one_or_none()

        deputy_deans_with_tr = await _fetch_people_with_tr(
            FacultyDeputyDean, FacultyDeputyDeanTr, "deputy_dean_id", faculty_code, lang_code, db
        )
        council_with_tr = await _fetch_people_with_tr(
            FacultyCouncilMember, FacultyCouncilMemberTr, "council_member_id", faculty_code, lang_code, db
        )
        workers_with_tr = await _fetch_people_with_tr(
            FacultyWorker, FacultyWorkerTr, "worker_id", faculty_code, lang_code, db
        )

        cafedra_count_query = await db.execute(
            select(func.count()).select_from(Cafedra).where(
                Cafedra.faculty_code == faculty_code
            )
        )
        cafedra_count = cafedra_count_query.scalar() or 0

        deputy_count_query = await db.execute(
            select(func.count()).select_from(FacultyDeputyDean).where(
                FacultyDeputyDean.faculty_code == faculty_code
            )
        )
        deputy_count = deputy_count_query.scalar() or 0

        faculty_obj = {
            "id": faculty.id,
            "faculty_code": faculty.faculty_code,

            # Statistics
            "bachelor_programs_count": faculty.bachelor_programs_count or 0,
            "master_programs_count": faculty.master_programs_count or 0,
            "phd_programs_count": faculty.phd_programs_count or 0,
            "international_collaborations_count": faculty.international_collaborations_count or 0,
            "laboratories_count": faculty.laboratories_count or 0,
            "projects_patents_count": faculty.projects_patents_count or 0,
            "industrial_collaborations_count": faculty.industrial_collaborations_count or 0,
            "sdgs": faculty.sdgs or [],
            "cafedra_count": cafedra_count,
            "deputy_dean_count": deputy_count,

            "director": await _serialize_director(director, lang_code, db) if director else None,
            "laboratories": await _serialize_translated_section(
                FacultyLaboratory, FacultyLaboratoryTr, "laboratory_id", faculty_code, lang_code, db,
            ),
            "research_works": await _serialize_translated_section(
                FacultyResearchWork, FacultyResearchWorkTr, "research_work_id", faculty_code, lang_code, db,
            ),
            "partner_companies": await _serialize_translated_section(
                FacultyPartnerCompany, FacultyPartnerCompanyTr, "partner_company_id", faculty_code, lang_code, db,
            ),
            "objectives": await _serialize_translated_section(
                FacultyObjective, FacultyObjectiveTr, "objective_id", faculty_code, lang_code, db,
            ),
            "duties": await _serialize_translated_section(
                FacultyDuty, FacultyDutyTr, "duty_id", faculty_code, lang_code, db,
            ),
            "projects": await _serialize_translated_section(
                FacultyProject, FacultyProjectTr, "project_id", faculty_code, lang_code, db,
            ),
            "directions_of_action": await _serialize_translated_section(
                FacultyDirectionOfAction, FacultyDirectionOfActionTr, "direction_of_action_id", faculty_code, lang_code, db,
            ),
            "deputy_deans": _serialize_people(deputy_deans_with_tr, lang_code, has_profile_image=True),
            "scientific_council": _serialize_people(council_with_tr, lang_code, has_profile_image=False),
            "workers": _serialize_people(workers_with_tr, lang_code, has_profile_image=True),
            "created_at": faculty.created_at.isoformat() if faculty.created_at else None,
            "updated_at": faculty.updated_at.isoformat() if faculty.updated_at else None,
        }

        if lang_code:
            faculty_obj["title"] = tr.faculty_name if tr else None
            faculty_obj["html_content"] = tr.about_text if tr else None
        else:
            for lc in ["az", "en"]:
                lc_tr = tr_bilingual.get(lc)
                faculty_obj[lc] = {
                    "title": lc_tr.faculty_name if lc_tr else None,
                    "html_content": lc_tr.about_text if lc_tr else None,
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

        # Update Statistics
        stat_fields = [
            "bachelor_programs_count",
            "master_programs_count",
            "phd_programs_count",
            "international_collaborations_count",
            "laboratories_count",
            "projects_patents_count",
            "industrial_collaborations_count",
        ]
        for field in stat_fields:
            if field in request_data:
                setattr(faculty, field, request_data[field])
        
        if "sdgs" in request_data:
            faculty.sdgs = validate_sdgs(request_data["sdgs"])

        if "director" in request_data:
            await _upsert_director(faculty_code, request_data.get("director"), now, db)

        if "laboratories" in request_data:
            await _delete_section(FacultyLaboratory, faculty_code, db)
            if request_data["laboratories"]:
                await _create_translated_section(
                    FacultyLaboratory, FacultyLaboratoryTr, "laboratory_id", faculty_code, request_data["laboratories"], now, db,
                )

        if "research_works" in request_data:
            await _delete_section(FacultyResearchWork, faculty_code, db)
            if request_data["research_works"]:
                await _create_translated_section(
                    FacultyResearchWork, FacultyResearchWorkTr, "research_work_id", faculty_code, request_data["research_works"], now, db,
                )

        if "partner_companies" in request_data:
            await _delete_section(FacultyPartnerCompany, faculty_code, db)
            if request_data["partner_companies"]:
                await _create_translated_section(
                    FacultyPartnerCompany, FacultyPartnerCompanyTr, "partner_company_id", faculty_code, request_data["partner_companies"], now, db,
                )

        if "objectives" in request_data:
            await _delete_section(FacultyObjective, faculty_code, db)
            if request_data["objectives"]:
                await _create_translated_section(
                    FacultyObjective, FacultyObjectiveTr, "objective_id", faculty_code, request_data["objectives"], now, db,
                )

        if "duties" in request_data:
            await _delete_section(FacultyDuty, faculty_code, db)
            if request_data["duties"]:
                await _create_translated_section(
                    FacultyDuty, FacultyDutyTr, "duty_id", faculty_code, request_data["duties"], now, db,
                )

        if "projects" in request_data:
            await _delete_section(FacultyProject, faculty_code, db)
            if request_data["projects"]:
                await _create_translated_section(
                    FacultyProject, FacultyProjectTr, "project_id", faculty_code, request_data["projects"], now, db,
                )

        if "directions_of_action" in request_data:
            await _delete_section(FacultyDirectionOfAction, faculty_code, db)
            if request_data["directions_of_action"]:
                await _create_translated_section(
                    FacultyDirectionOfAction, FacultyDirectionOfActionTr, "direction_of_action_id", faculty_code, request_data["directions_of_action"], now, db,
                )

        if "deputy_deans" in request_data:
            await _delete_section(FacultyDeputyDean, faculty_code, db)
            if request_data["deputy_deans"]:
                await _create_people(FacultyDeputyDean, FacultyDeputyDeanTr, "deputy_dean_id", request_data["deputy_deans"], faculty_code, now, db)

        if "scientific_council" in request_data:
            await _delete_section(FacultyCouncilMember, faculty_code, db)
            if request_data["scientific_council"]:
                await _create_people(FacultyCouncilMember, FacultyCouncilMemberTr, "council_member_id", request_data["scientific_council"], faculty_code, now, db)

        if "workers" in request_data:
            await _delete_section(FacultyWorker, faculty_code, db)
            if request_data["workers"]:
                await _create_people(FacultyWorker, FacultyWorkerTr, "worker_id", request_data["workers"], faculty_code, now, db)

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


# ── New service functions ──────────────────────────────────────────────────────


async def upload_director_profile_image(
    faculty_code: str,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        director_query = await db.execute(
            select(FacultyDirector).where(FacultyDirector.faculty_code == faculty_code)
        )
        director = director_query.scalar_one_or_none()

        if not director:
            return JSONResponse(
                content={"status_code": 404, "message": "Director not found for this faculty."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = director.profile_image
        new_path = await save_upload(image, "directors", ALLOWED_IMAGE_MIMES)

        director.profile_image = new_path
        director.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Director profile image uploaded successfully.",
                "data": {"profile_image": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_deputy_dean_profile_image(
    deputy_dean_id: int,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        query = await db.execute(
            select(FacultyDeputyDean).where(FacultyDeputyDean.id == deputy_dean_id)
        )
        deputy_dean = query.scalar_one_or_none()

        if not deputy_dean:
            return JSONResponse(
                content={"status_code": 404, "message": "Deputy dean not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = deputy_dean.profile_image
        new_path = await save_upload(image, "deputy-deans", ALLOWED_IMAGE_MIMES)

        deputy_dean.profile_image = new_path
        deputy_dean.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Deputy dean profile image uploaded successfully.",
                "data": {"profile_image": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_worker_profile_image(
    worker_id: int,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        query = await db.execute(
            select(FacultyWorker).where(FacultyWorker.id == worker_id)
        )
        worker = query.scalar_one_or_none()

        if not worker:
            return JSONResponse(
                content={"status_code": 404, "message": "Worker not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = worker.profile_image
        new_path = await save_upload(image, "faculty-workers", ALLOWED_IMAGE_MIMES)

        worker.profile_image = new_path
        worker.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Worker profile image uploaded successfully.",
                "data": {"profile_image": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_directions_of_action(
    faculty_code: str,
    lang_code: str,
    db: AsyncSession,
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        if not faculty_query.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        items = await _serialize_translated_section(
            FacultyDirectionOfAction,
            FacultyDirectionOfActionTr,
            "direction_of_action_id",
            faculty_code,
            lang_code,
            db,
        )
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Directions of action fetched successfully.",
                "directions_of_action": items,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def create_direction_of_action(
    faculty_code: str,
    request: CreateDirectionOfAction,
    db: AsyncSession,
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        if not faculty_query.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)
        direction = FacultyDirectionOfAction(
            faculty_code=faculty_code,
            display_order=0,
            created_at=now,
            updated_at=now,
        )
        db.add(direction)
        await db.flush()

        db.add(FacultyDirectionOfActionTr(
            direction_of_action_id=direction.id,
            lang_code="az",
            title=request.az.title,
            description=request.az.description,
            created_at=now,
            updated_at=now,
        ))
        db.add(FacultyDirectionOfActionTr(
            direction_of_action_id=direction.id,
            lang_code="en",
            title=request.en.title,
            description=request.en.description,
            created_at=now,
            updated_at=now,
        ))

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Direction of action created successfully.",
                "data": {"id": direction.id},
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_direction_of_action(
    direction_id: int,
    request: UpdateDirectionOfAction,
    db: AsyncSession,
):
    try:
        direction_query = await db.execute(
            select(FacultyDirectionOfAction).where(FacultyDirectionOfAction.id == direction_id)
        )
        direction = direction_query.scalar_one_or_none()

        if not direction:
            return JSONResponse(
                content={"status_code": 404, "message": "Direction of action not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)
        data = request.dict(exclude_unset=True)

        for lang, payload in [("az", data.get("az")), ("en", data.get("en"))]:
            if payload is None:
                continue
            tr_query = await db.execute(
                select(FacultyDirectionOfActionTr).where(
                    FacultyDirectionOfActionTr.direction_of_action_id == direction_id,
                    FacultyDirectionOfActionTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()
            if tr:
                if "title" in payload:
                    tr.title = payload["title"]
                if "description" in payload:
                    tr.description = payload["description"]
                tr.updated_at = now
            else:
                db.add(FacultyDirectionOfActionTr(
                    direction_of_action_id=direction_id,
                    lang_code=lang,
                    title=payload.get("title", ""),
                    description=payload.get("description"),
                    created_at=now,
                    updated_at=now,
                ))

        direction.updated_at = now
        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Direction of action updated successfully."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_direction_of_action(
    direction_id: int,
    db: AsyncSession,
):
    try:
        direction_query = await db.execute(
            select(FacultyDirectionOfAction).where(FacultyDirectionOfAction.id == direction_id)
        )
        if not direction_query.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Direction of action not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await db.execute(
            sqlalchemy_delete(FacultyDirectionOfAction).where(FacultyDirectionOfAction.id == direction_id)
        )
        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Direction of action deleted successfully."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def create_worker(
    faculty_code: str,
    request: Worker,
    db: AsyncSession,
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        if not faculty_query.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Faculty not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)
        worker = FacultyWorker(
            faculty_code=faculty_code,
            first_name=request.first_name,
            last_name=request.last_name,
            father_name=request.father_name,
            email=request.email,
            phone=request.phone,
            profile_image=request.profile_image,
            created_at=now,
            updated_at=now,
        )
        db.add(worker)
        await db.flush()

        for lang_code, tr_data in [("az", request.az), ("en", request.en)]:
            if tr_data is None:
                continue
            db.add(FacultyWorkerTr(
                worker_id=worker.id,
                lang_code=lang_code,
                duty=tr_data.duty,
                scientific_name=tr_data.scientific_name,
                scientific_degree=tr_data.scientific_degree,
                created_at=now,
                updated_at=now,
            ))

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Worker added successfully.",
                "data": {"id": worker.id},
            },
            status_code=status.HTTP_201_CREATED,
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
