import secrets
from datetime import datetime, timezone
from typing import Any, Type

from fastapi import Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.cafedra import CreateCafedra, UpdateCafedra
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload
from app.core.logger import get_logger
from app.core.session import get_db
from app.models.faculties.faculties import Faculty
from app.models.cafedras.cafedras import Cafedra
from app.models.cafedras.cafedras_tr import CafedraTr
from app.models.cafedras.cafedra_director import (
    CafedraDirector,
    CafedraDirectorTr,
    CafedraDirectorWorkingHour,
    CafedraDirectorWorkingHourTr,
    CafedraDirectorEducation,
    CafedraDirectorEducationTr,
)
from app.models.cafedras.cafedra_personnel import (
    CafedraWorker,
    CafedraWorkerTr,
)
from app.models.cafedras.cafedra_section import (
    CafedraDirectionOfAction,
    CafedraDirectionOfActionTr,
)
from app.utils.language import get_language

logger = get_logger(__name__)


def validate_sdgs(sdgs: list[int] | None) -> list[int]:
    if not sdgs:
        return []
    valid_sdgs = [i for i in sdgs if 1 <= i <= 17]
    return list(set(valid_sdgs))


def cafedra_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


async def _create_translated_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    cafedra_code: str,
    items: list[Any],
    now: datetime,
    db: AsyncSession,
):
    for index, item in enumerate(items):
        parent = parent_cls(
            cafedra_code=cafedra_code,
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(parent)
        await db.flush()

        for lang in ["az", "en"]:
            data = getattr(item, lang)
            db.add(
                tr_cls(
                    **{
                        parent_id_name: parent.id,
                        "lang_code": lang,
                        "title": data.title,
                        "description": data.description,
                        "created_at": now,
                        "updated_at": now,
                    }
                )
            )


async def _serialize_translated_section(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    parent_id_name: str,
    cafedra_code: str,
    lang_code: str,
    db: AsyncSession,
):
    items = []
    parents_query = await db.execute(
        select(parent_cls).where(parent_cls.cafedra_code == cafedra_code).order_by(parent_cls.display_order.asc())
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


async def _create_people(
    parent_cls: Type[Any],
    tr_cls: Type[Any],
    person_id_field: str,
    items: list[Any],
    cafedra_code: str,
    now: datetime,
    db: AsyncSession,
):
    for item in items:
        person = parent_cls(
            cafedra_code=cafedra_code,
            first_name=item.first_name,
            last_name=item.last_name,
            father_name=item.father_name,
            email=getattr(item, "email", None),
            phone=getattr(item, "phone", None),
            profile_image=getattr(item, "profile_image", None),
            created_at=now,
            updated_at=now,
        )
        db.add(person)
        await db.flush()

        for lang in ["az", "en"]:
            data = getattr(item, lang)
            if data:
                fields = {
                    person_id_field: person.id,
                    "lang_code": lang,
                    "duty": data.duty,
                    "created_at": now,
                    "updated_at": now,
                }
                if hasattr(tr_cls, "scientific_name"):
                    fields["scientific_name"] = data.scientific_name
                if hasattr(tr_cls, "scientific_degree"):
                    fields["scientific_degree"] = data.scientific_degree
                db.add(tr_cls(**fields))


async def _create_director(cafedra_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director = CafedraDirector(
        cafedra_code=cafedra_code,
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

    for lang in ["az", "en"]:
        tr_data = getattr(director_data, lang)
        if tr_data:
            db.add(CafedraDirectorTr(
                director_id=director.id,
                lang_code=lang,
                scientific_degree=tr_data.scientific_degree,
                scientific_title=tr_data.scientific_title,
                bio=tr_data.bio,
                scientific_research_fields=tr_data.scientific_research_fields or [],
                created_at=now,
                updated_at=now,
            ))

    if director_data.working_hours:
        for item in director_data.working_hours:
            wh = CafedraDirectorWorkingHour(
                director_id=director.id,
                time_range=item.time_range,
                created_at=now,
                updated_at=now,
            )
            db.add(wh)
            await db.flush()
            db.add(CafedraDirectorWorkingHourTr(
                working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now,
            ))
            db.add(CafedraDirectorWorkingHourTr(
                working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now,
            ))

    if director_data.educations:
        for item in director_data.educations:
            edu = CafedraDirectorEducation(
                director_id=director.id,
                start_year=item.start_year,
                end_year=item.end_year,
                created_at=now,
                updated_at=now,
            )
            db.add(edu)
            await db.flush()
            db.add(CafedraDirectorEducationTr(
                education_id=edu.id,
                lang_code="az",
                degree=item.az.degree,
                university=item.az.university,
                created_at=now,
                updated_at=now,
            ))
            db.add(CafedraDirectorEducationTr(
                education_id=edu.id,
                lang_code="en",
                degree=item.en.degree,
                university=item.en.university,
                created_at=now,
                updated_at=now,
            ))


async def _upsert_director(cafedra_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director_query = await db.execute(
        select(CafedraDirector).where(CafedraDirector.cafedra_code == cafedra_code)
    )
    director = director_query.scalar_one_or_none()

    if director_data is None:
        if director:
            await db.execute(sqlalchemy_delete(CafedraDirector).where(CafedraDirector.id == director.id))
        return None

    if not director:
        director = CafedraDirector(cafedra_code=cafedra_code, created_at=now, updated_at=now)
        db.add(director)
        await db.flush()

    data = director_data.dict(exclude_unset=True)
    for field in ["first_name", "last_name", "father_name", "email", "phone", "room_number", "profile_image"]:
        if field in data:
            setattr(director, field, data[field])
    director.updated_at = now

    for lang in ["az", "en"]:
        tr_data = data.get(lang)
        if tr_data:
            tr_query = await db.execute(
                select(CafedraDirectorTr).where(
                    CafedraDirectorTr.director_id == director.id,
                    CafedraDirectorTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()
            if tr:
                for field in ["scientific_degree", "scientific_title", "bio", "scientific_research_fields"]:
                    if field in tr_data:
                        setattr(tr, field, tr_data[field])
                tr.updated_at = now
            else:
                db.add(CafedraDirectorTr(
                    director_id=director.id,
                    lang_code=lang,
                    scientific_degree=tr_data.get("scientific_degree"),
                    scientific_title=tr_data.get("scientific_title"),
                    bio=tr_data.get("bio"),
                    scientific_research_fields=tr_data.get("scientific_research_fields") or [],
                    created_at=now,
                    updated_at=now,
                ))

    if "working_hours" in data:
        await db.execute(sqlalchemy_delete(CafedraDirectorWorkingHour).where(CafedraDirectorWorkingHour.director_id == director.id))
        if data["working_hours"]:
            for item in data["working_hours"]:
                wh = CafedraDirectorWorkingHour(director_id=director.id, time_range=item.time_range, created_at=now, updated_at=now)
                db.add(wh)
                await db.flush()
                db.add(CafedraDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="az", day=item.az.day, created_at=now, updated_at=now))
                db.add(CafedraDirectorWorkingHourTr(working_hour_id=wh.id, lang_code="en", day=item.en.day, created_at=now, updated_at=now))

    if "educations" in data:
        await db.execute(sqlalchemy_delete(CafedraDirectorEducation).where(CafedraDirectorEducation.director_id == director.id))
        if data["educations"]:
            for item in data["educations"]:
                edu = CafedraDirectorEducation(director_id=director.id, start_year=item.start_year, end_year=item.end_year, created_at=now, updated_at=now)
                db.add(edu)
                await db.flush()
                db.add(CafedraDirectorEducationTr(education_id=edu.id, lang_code="az", degree=item.az.degree, university=item.az.university, created_at=now, updated_at=now))
                db.add(CafedraDirectorEducationTr(education_id=edu.id, lang_code="en", degree=item.en.degree, university=item.en.university, created_at=now, updated_at=now))

    return director


async def _serialize_director(director: CafedraDirector, lang_code: str, db: AsyncSession):
    if not director:
        return None

    tr_query = await db.execute(
        select(CafedraDirectorTr).where(
            CafedraDirectorTr.director_id == director.id,
            CafedraDirectorTr.lang_code == lang_code,
        )
    )
    tr = tr_query.scalar_one_or_none()

    working_hours_query = await db.execute(select(CafedraDirectorWorkingHour).where(CafedraDirectorWorkingHour.director_id == director.id))
    educations_query = await db.execute(select(CafedraDirectorEducation).where(CafedraDirectorEducation.director_id == director.id))

    working_hours = []
    for hour in working_hours_query.scalars().all():
        wh_tr_q = await db.execute(select(CafedraDirectorWorkingHourTr).where(CafedraDirectorWorkingHourTr.working_hour_id == hour.id, CafedraDirectorWorkingHourTr.lang_code == lang_code))
        wh_tr = wh_tr_q.scalar_one_or_none()
        working_hours.append({"day": wh_tr.day if wh_tr else None, "time_range": hour.time_range})

    educations = []
    for edu in educations_query.scalars().all():
        edu_tr_q = await db.execute(select(CafedraDirectorEducationTr).where(CafedraDirectorEducationTr.education_id == edu.id, CafedraDirectorEducationTr.lang_code == lang_code))
        edu_tr = edu_tr_q.scalar_one_or_none()
        educations.append({"degree": edu_tr.degree if edu_tr else None, "university": edu_tr.university if edu_tr else None, "start_year": edu.start_year, "end_year": edu.end_year})

    return {
        "first_name": director.first_name,
        "last_name": director.last_name,
        "father_name": director.father_name,
        "scientific_degree": tr.scientific_degree if tr else None,
        "scientific_title": tr.scientific_title if tr else None,
        "bio": tr.bio if tr else None,
        "scientific_research_fields": tr.scientific_research_fields if tr else [],
        "email": director.email,
        "phone": director.phone,
        "room_number": director.room_number,
        "profile_image": director.profile_image,
        "working_hours": working_hours,
        "educations": educations,
    }


async def create_cafedra(
    request: CreateCafedra,
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(select(Faculty).where(Faculty.faculty_code == request.faculty_code))
        if not faculty_query.scalar_one_or_none():
            return JSONResponse(content={"status_code": 404, "message": "Faculty not found."}, status_code=status.HTTP_404_NOT_FOUND)

        cafedra_code = None
        for _ in range(10):
            candidate = cafedra_code_generator()
            existing_query = await db.execute(select(Cafedra).where(Cafedra.cafedra_code == candidate))
            if not existing_query.scalar_one_or_none():
                cafedra_code = candidate
                break

        if not cafedra_code:
            return JSONResponse(content={"status_code": 500, "message": "Failed to generate unique cafedra code."}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        now = datetime.now(timezone.utc)
        cafedra = Cafedra(
            faculty_code=request.faculty_code,
            cafedra_code=cafedra_code,
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
        db.add(cafedra)

        db.add(CafedraTr(cafedra_code=cafedra_code, lang_code="az", cafedra_name=request.az.title, about_text=request.az.html_content, created_at=now))
        db.add(CafedraTr(cafedra_code=cafedra_code, lang_code="en", cafedra_name=request.en.title, about_text=request.en.html_content, created_at=now))

        if request.director:
            await _create_director(cafedra_code, request.director, now, db)

        if request.directions_of_action:
            await _create_translated_section(CafedraDirectionOfAction, CafedraDirectionOfActionTr, "direction_of_action_id", cafedra_code, request.directions_of_action, now, db)

        if request.workers:
            await _create_people(CafedraWorker, CafedraWorkerTr, "worker_id", request.workers, cafedra_code, now, db)

        await db.commit()
        await db.refresh(cafedra)

        return JSONResponse(
            content={
                "status_code": 201,
                "data": {"cafedra_code": cafedra.cafedra_code, "created_at": cafedra.created_at.isoformat()},
                "message": "Cafedra created successfully.",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_cafedras(
    start: int = 0,
    end: int = 10,
    faculty_code: str | None = None,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        query = select(Cafedra)
        if faculty_code:
            query = query.where(Cafedra.faculty_code == faculty_code)
        
        total_query = await db.execute(select(func.count()).select_from(query.subquery()))
        total = total_query.scalar() or 0

        cafedra_query = await db.execute(query.order_by(Cafedra.id.asc()).offset(start).limit(end - start))
        cafedras = cafedra_query.scalars().all()

        if not cafedras:
            return JSONResponse(content={"status_code": 204, "message": "No content."}, status_code=status.HTTP_204_NO_CONTENT)

        cafedras_arr = []
        for cafedra in cafedras:
            tr_query = await db.execute(select(CafedraTr).where(CafedraTr.cafedra_code == cafedra.cafedra_code, CafedraTr.lang_code == lang))
            tr = tr_query.scalar_one_or_none()

            cafedras_arr.append({
                "id": cafedra.id,
                "faculty_code": cafedra.faculty_code,
                "cafedra_code": cafedra.cafedra_code,
                "title": tr.cafedra_name if tr else None,
                "created_at": cafedra.created_at.isoformat() if cafedra.created_at else None,
            })

        return JSONResponse(content={"status_code": 200, "message": "Cafedras fetched successfully.", "cafedras": cafedras_arr, "total": total}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_cafedra(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        cafedra_query = await db.execute(select(Cafedra).where(Cafedra.cafedra_code == cafedra_code))
        cafedra = cafedra_query.scalar_one_or_none()

        if not cafedra:
            return JSONResponse(content={"status_code": 404, "message": "Cafedra not found."}, status_code=status.HTTP_404_NOT_FOUND)

        tr_query = await db.execute(select(CafedraTr).where(CafedraTr.cafedra_code == cafedra_code, CafedraTr.lang_code == lang_code))
        tr = tr_query.scalar_one_or_none()

        director_query = await db.execute(select(CafedraDirector).where(CafedraDirector.cafedra_code == cafedra_code))
        director = director_query.scalar_one_or_none()

        workers_query = await db.execute(select(CafedraWorker).where(CafedraWorker.cafedra_code == cafedra_code))
        workers = workers_query.scalars().all()
        workers_list = []
        for worker in workers:
            w_tr_q = await db.execute(select(CafedraWorkerTr).where(CafedraWorkerTr.worker_id == worker.id, CafedraWorkerTr.lang_code == lang_code))
            w_tr = w_tr_q.scalar_one_or_none()
            workers_list.append({
                "first_name": worker.first_name,
                "last_name": worker.last_name,
                "father_name": worker.father_name,
                "duty": w_tr.duty if w_tr else None,
                "scientific_name": w_tr.scientific_name if w_tr else None,
                "scientific_degree": w_tr.scientific_degree if w_tr else None,
                "email": worker.email,
                "phone": worker.phone,
                "profile_image": worker.profile_image,
            })

        cafedra_obj = {
            "id": cafedra.id,
            "faculty_code": cafedra.faculty_code,
            "cafedra_code": cafedra.cafedra_code,
            "title": tr.cafedra_name if tr else None,
            "html_content": tr.about_text if tr else None,
            "bachelor_programs_count": cafedra.bachelor_programs_count,
            "master_programs_count": cafedra.master_programs_count,
            "phd_programs_count": cafedra.phd_programs_count,
            "international_collaborations_count": cafedra.international_collaborations_count,
            "laboratories_count": cafedra.laboratories_count,
            "projects_patents_count": cafedra.projects_patents_count,
            "industrial_collaborations_count": cafedra.industrial_collaborations_count,
            "sdgs": cafedra.sdgs,
            "director": await _serialize_director(director, lang_code, db) if director else None,
            "directions_of_action": await _serialize_translated_section(CafedraDirectionOfAction, CafedraDirectionOfActionTr, "direction_of_action_id", cafedra_code, lang_code, db),
            "workers": workers_list,
            "created_at": cafedra.created_at.isoformat() if cafedra.created_at else None,
            "updated_at": cafedra.updated_at.isoformat() if cafedra.updated_at else None,
        }

        return JSONResponse(content={"status_code": 200, "message": "Cafedra details fetched successfully.", "cafedra": cafedra_obj}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_cafedra(
    cafedra_code: str,
    request: UpdateCafedra,
    db: AsyncSession = Depends(get_db),
):
    try:
        cafedra_query = await db.execute(select(Cafedra).where(Cafedra.cafedra_code == cafedra_code))
        cafedra = cafedra_query.scalar_one_or_none()

        if not cafedra:
            return JSONResponse(content={"status_code": 404, "message": "Cafedra not found."}, status_code=status.HTTP_404_NOT_FOUND)

        request_data = request.dict(exclude_unset=True)
        now = datetime.now(timezone.utc)

        for lang in ["az", "en"]:
            tr_payload = request_data.get(lang)
            if tr_payload:
                tr_query = await db.execute(select(CafedraTr).where(CafedraTr.cafedra_code == cafedra_code, CafedraTr.lang_code == lang))
                tr = tr_query.scalar_one_or_none()
                if tr:
                    if "title" in tr_payload: tr.cafedra_name = tr_payload["title"]
                    if "html_content" in tr_payload: tr.about_text = tr_payload["html_content"]
                    tr.updated_at = now
                else:
                    db.add(CafedraTr(cafedra_code=cafedra_code, lang_code=lang, cafedra_name=tr_payload.get("title", ""), about_text=tr_payload.get("html_content"), created_at=now))

        stat_fields = ["bachelor_programs_count", "master_programs_count", "phd_programs_count", "international_collaborations_count", "laboratories_count", "projects_patents_count", "industrial_collaborations_count"]
        for field in stat_fields:
            if field in request_data:
                setattr(cafedra, field, request_data[field])
        
        if "sdgs" in request_data:
            cafedra.sdgs = validate_sdgs(request_data["sdgs"])

        if "director" in request_data:
            await _upsert_director(cafedra_code, request.director, now, db)

        if "directions_of_action" in request_data:
            await db.execute(sqlalchemy_delete(CafedraDirectionOfAction).where(CafedraDirectionOfAction.cafedra_code == cafedra_code))
            if request_data["directions_of_action"]:
                await _create_translated_section(CafedraDirectionOfAction, CafedraDirectionOfActionTr, "direction_of_action_id", cafedra_code, request.directions_of_action, now, db)

        if "workers" in request_data:
            await db.execute(sqlalchemy_delete(CafedraWorker).where(CafedraWorker.cafedra_code == cafedra_code))
            if request_data["workers"]:
                await _create_people(CafedraWorker, CafedraWorkerTr, "worker_id", request.workers, cafedra_code, now, db)

        cafedra.updated_at = now
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Cafedra updated successfully."}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def delete_cafedra(cafedra_code: str, db: AsyncSession = Depends(get_db)):
    try:
        cafedra_query = await db.execute(select(Cafedra).where(Cafedra.cafedra_code == cafedra_code))
        if not cafedra_query.scalar_one_or_none():
            return JSONResponse(content={"status_code": 404, "message": "Cafedra not found."}, status_code=status.HTTP_404_NOT_FOUND)

        await db.execute(sqlalchemy_delete(CafedraTr).where(CafedraTr.cafedra_code == cafedra_code))
        await db.execute(sqlalchemy_delete(Cafedra).where(Cafedra.cafedra_code == cafedra_code))
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Cafedra deleted successfully."}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def upload_cafedra_director_image(cafedra_code: str, image: UploadFile, db: AsyncSession):
    try:
        director_query = await db.execute(select(CafedraDirector).where(CafedraDirector.cafedra_code == cafedra_code))
        director = director_query.scalar_one_or_none()
        if not director: return JSONResponse(content={"status_code": 404, "message": "Director not found."}, status_code=status.HTTP_404_NOT_FOUND)
        old_path = director.profile_image
        new_path = await save_upload(image, "cafedra-directors", ALLOWED_IMAGE_MIMES)
        director.profile_image = new_path
        director.updated_at = datetime.now(timezone.utc)
        await db.commit()
        if old_path: safe_delete_file(old_path)
        return JSONResponse(content={"status_code": 200, "message": "Director profile image uploaded successfully.", "data": {"profile_image": new_path}}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def upload_cafedra_worker_image(worker_id: int, image: UploadFile, db: AsyncSession):
    try:
        query = await db.execute(select(CafedraWorker).where(CafedraWorker.id == worker_id))
        worker = query.scalar_one_or_none()
        if not worker: return JSONResponse(content={"status_code": 404, "message": "Worker not found."}, status_code=status.HTTP_404_NOT_FOUND)
        old_path = worker.profile_image
        new_path = await save_upload(image, "cafedra-workers", ALLOWED_IMAGE_MIMES)
        worker.profile_image = new_path
        worker.updated_at = datetime.now(timezone.utc)
        await db.commit()
        if old_path: safe_delete_file(old_path)
        return JSONResponse(content={"status_code": 200, "message": "Worker profile image uploaded successfully.", "data": {"profile_image": new_path}}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
