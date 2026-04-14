import secrets
from datetime import datetime, timezone
from typing import Any

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.research_institute import (
    CreateResearchInstitute,
    UpdateResearchInstitute,
)
from app.core.logger import get_logger
from app.models.research_institute.institute import (
    ResearchInstitute,
    ResearchInstituteTr,
    InstituteDirector,
    InstituteDirectorTr,
    InstituteDirectorEducation,
    InstituteDirectorEducationTr,
    InstituteStaff,
    InstituteStaffTr,
)
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload

logger = get_logger(__name__)


def _institute_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


# ── Director helpers ───────────────────────────────────────────────────────────


async def _create_director(institute_code: str, data: Any, now: datetime, db: AsyncSession):
    director = InstituteDirector(
        institute_code=institute_code,
        first_name=data.first_name,
        last_name=data.last_name,
        father_name=data.father_name,
        email=data.email,
        room_number=data.room_number,
        image=data.image,
        created_at=now,
        updated_at=now,
    )
    db.add(director)
    await db.flush()

    for lang_code, tr_data in [("az", data.az), ("en", data.en)]:
        db.add(InstituteDirectorTr(
            director_id=director.id,
            lang_code=lang_code,
            scientific_name=tr_data.scientific_name,
            scientific_degree=tr_data.scientific_degree,
            bio=tr_data.bio,
            researcher_areas=tr_data.researcher_areas,
            created_at=now,
            updated_at=now,
        ))

    if data.educations:
        for item in data.educations:
            edu = InstituteDirectorEducation(
                director_id=director.id,
                university_name=item.university_name,
                start_year=item.start_year,
                end_year=item.end_year,
                created_at=now,
                updated_at=now,
            )
            db.add(edu)
            await db.flush()
            db.add(InstituteDirectorEducationTr(education_id=edu.id, lang_code="az", degree=item.az.degree, created_at=now, updated_at=now))
            db.add(InstituteDirectorEducationTr(education_id=edu.id, lang_code="en", degree=item.en.degree, created_at=now, updated_at=now))

    return director


async def _upsert_director(institute_code: str, director_data: Any, now: datetime, db: AsyncSession):
    director_q = await db.execute(
        select(InstituteDirector).where(InstituteDirector.institute_code == institute_code)
    )
    director = director_q.scalar_one_or_none()

    if director_data is None:
        if director:
            await db.execute(sqlalchemy_delete(InstituteDirector).where(InstituteDirector.id == director.id))
        return None

    if not director:
        director = InstituteDirector(institute_code=institute_code, created_at=now, updated_at=now)
        db.add(director)
        await db.flush()

    data = director_data.dict(exclude_unset=True)
    for field in ["first_name", "last_name", "father_name", "email", "room_number", "image"]:
        if field in data:
            setattr(director, field, data[field])
    director.updated_at = now

    for lang_code in ["az", "en"]:
        tr_data = data.get(lang_code)
        if tr_data:
            tr_q = await db.execute(
                select(InstituteDirectorTr).where(
                    InstituteDirectorTr.director_id == director.id,
                    InstituteDirectorTr.lang_code == lang_code,
                )
            )
            tr = tr_q.scalar_one_or_none()
            if tr:
                for field in ["scientific_name", "scientific_degree", "bio", "researcher_areas"]:
                    if field in tr_data:
                        setattr(tr, field, tr_data[field])
                tr.updated_at = now
            else:
                db.add(InstituteDirectorTr(
                    director_id=director.id,
                    lang_code=lang_code,
                    **tr_data,
                    created_at=now,
                    updated_at=now,
                ))

    if "educations" in data:
        await db.execute(sqlalchemy_delete(InstituteDirectorEducation).where(InstituteDirectorEducation.director_id == director.id))
        for item in (data["educations"] or []):
            edu = InstituteDirectorEducation(director_id=director.id, university_name=item.university_name, start_year=item.start_year, end_year=item.end_year, created_at=now, updated_at=now)
            db.add(edu)
            await db.flush()
            db.add(InstituteDirectorEducationTr(education_id=edu.id, lang_code="az", degree=item.az.degree, created_at=now, updated_at=now))
            db.add(InstituteDirectorEducationTr(education_id=edu.id, lang_code="en", degree=item.en.degree, created_at=now, updated_at=now))

    return director


async def _serialize_director(director: InstituteDirector, lang_code: str, db: AsyncSession) -> dict | None:
    if not director:
        return None

    tr_q = await db.execute(
        select(InstituteDirectorTr).where(
            InstituteDirectorTr.director_id == director.id,
            InstituteDirectorTr.lang_code == lang_code,
        )
    )
    tr = tr_q.scalar_one_or_none()

    edu_q = await db.execute(select(InstituteDirectorEducation).where(InstituteDirectorEducation.director_id == director.id))
    educations = []
    for edu in edu_q.scalars().all():
        edu_tr_q = await db.execute(
            select(InstituteDirectorEducationTr).where(
                InstituteDirectorEducationTr.education_id == edu.id,
                InstituteDirectorEducationTr.lang_code == lang_code,
            )
        )
        edu_tr = edu_tr_q.scalar_one_or_none()
        educations.append({
            "university_name": edu.university_name,
            "degree": edu_tr.degree if edu_tr else None,
            "start_year": edu.start_year,
            "end_year": edu.end_year,
        })

    return {
        "id": director.id,
        "first_name": director.first_name,
        "last_name": director.last_name,
        "father_name": director.father_name,
        "email": director.email,
        "room_number": director.room_number,
        "image": director.image,
        "scientific_name": tr.scientific_name if tr else None,
        "scientific_degree": tr.scientific_degree if tr else None,
        "bio": tr.bio if tr else None,
        "researcher_areas": tr.researcher_areas if tr else None,
        "educations": educations,
    }


# ── Staff helpers ─────────────────────────────────────────────────────────────


async def _create_staff(institute_code: str, staff: list[Any], now: datetime, db: AsyncSession):
    for item in staff:
        member = InstituteStaff(
            institute_code=institute_code,
            first_name=item.first_name,
            last_name=item.last_name,
            father_name=item.father_name,
            email=item.email,
            phone_number=item.phone_number,
            image=item.image,
            created_at=now,
            updated_at=now,
        )
        db.add(member)
        await db.flush()

        for lang_code, tr_data in [("az", item.az), ("en", item.en)]:
            db.add(InstituteStaffTr(
                staff_id=member.id,
                lang_code=lang_code,
                scientific_name=tr_data.scientific_name,
                scientific_degree=tr_data.scientific_degree,
                created_at=now,
                updated_at=now,
            ))


async def _serialize_staff(institute_code: str, lang_code: str, db: AsyncSession) -> list[dict]:
    staff_q = await db.execute(select(InstituteStaff).where(InstituteStaff.institute_code == institute_code))
    result = []
    for member in staff_q.scalars().all():
        tr_q = await db.execute(
            select(InstituteStaffTr).where(
                InstituteStaffTr.staff_id == member.id,
                InstituteStaffTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()
        result.append({
            "id": member.id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "father_name": member.father_name,
            "email": member.email,
            "phone_number": member.phone_number,
            "image": member.image,
            "scientific_name": tr.scientific_name if tr else None,
            "scientific_degree": tr.scientific_degree if tr else None,
        })
    return result


# ── Public service functions ───────────────────────────────────────────────────


async def create_research_institute(request: CreateResearchInstitute, db: AsyncSession):
    try:
        institute_code = None
        for _ in range(10):
            candidate = _institute_code_generator()
            existing_q = await db.execute(select(ResearchInstitute).where(ResearchInstitute.institute_code == candidate))
            if not existing_q.scalar_one_or_none():
                institute_code = candidate
                break

        if not institute_code:
            return JSONResponse(
                content={"status_code": 500, "message": "Failed to generate unique institute code."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        now = datetime.now(timezone.utc)
        institute = ResearchInstitute(institute_code=institute_code, image=request.image, created_at=now, updated_at=now)
        db.add(institute)

        for lang_code, translation in [("az", request.az), ("en", request.en)]:
            db.add(ResearchInstituteTr(
                institute_code=institute_code,
                lang_code=lang_code,
                name=translation.name,
                about_html=translation.about_html,
                vision_html=translation.vision_html,
                mission_html=translation.mission_html,
                goals_html=translation.goals_html,
                direction_html=translation.direction_html,
                created_at=now,
                updated_at=now,
            ))

        if request.director:
            await _create_director(institute_code, request.director, now, db)

        if request.staff:
            await _create_staff(institute_code, request.staff, now, db)

        await db.commit()
        await db.refresh(institute)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Research Institute created successfully.",
                "data": {"institute_code": institute.institute_code, "created_at": institute.created_at.isoformat()},
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


async def get_research_institutes(start: int, end: int, lang: str, db: AsyncSession):
    try:
        total_q = await db.execute(select(func.count()).select_from(ResearchInstitute))
        total = total_q.scalar() or 0

        inst_q = await db.execute(
            select(ResearchInstitute).order_by(ResearchInstitute.id.asc()).offset(start).limit(end - start)
        )
        institutes = inst_q.scalars().all()

        if not institutes:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        result = []
        for inst in institutes:
            tr_q = await db.execute(
                select(ResearchInstituteTr).where(
                    ResearchInstituteTr.institute_code == inst.institute_code,
                    ResearchInstituteTr.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()

            staff_count_q = await db.execute(
                select(func.count()).select_from(InstituteStaff).where(InstituteStaff.institute_code == inst.institute_code)
            )
            staff_count = staff_count_q.scalar() or 0

            result.append({
                "id": inst.id,
                "institute_code": inst.institute_code,
                "name": tr.name if tr else None,
                "staff_count": staff_count,
                "created_at": inst.created_at.isoformat() if inst.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "Research Institutes fetched successfully.", "institutes": result, "total": total},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_institute(institute_code: str, lang_code: str, db: AsyncSession):
    try:
        inst_q = await db.execute(select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code))
        institute = inst_q.scalar_one_or_none()

        if not institute:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(ResearchInstituteTr).where(
                ResearchInstituteTr.institute_code == institute_code,
                ResearchInstituteTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()

        director_q = await db.execute(select(InstituteDirector).where(InstituteDirector.institute_code == institute_code))
        director = director_q.scalar_one_or_none()

        inst_obj = {
            "id": institute.id,
            "institute_code": institute.institute_code,
            "image": institute.image,
            "name": tr.name if tr else None,
            "about_html": tr.about_html if tr else None,
            "vision_html": tr.vision_html if tr else None,
            "mission_html": tr.mission_html if tr else None,
            "goals_html": tr.goals_html if tr else None,
            "direction_html": tr.direction_html if tr else None,
            "director": await _serialize_director(director, lang_code, db),
            "staff": await _serialize_staff(institute_code, lang_code, db),
            "created_at": institute.created_at.isoformat() if institute.created_at else None,
            "updated_at": institute.updated_at.isoformat() if institute.updated_at else None,
        }

        return JSONResponse(
            content={"status_code": 200, "message": "Research Institute fetched successfully.", "institute": inst_obj},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_research_institute(institute_code: str, request: UpdateResearchInstitute, db: AsyncSession):
    try:
        inst_q = await db.execute(select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code))
        institute = inst_q.scalar_one_or_none()

        if not institute:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data = request.dict(exclude_unset=True)
        now = datetime.now(timezone.utc)

        if "image" in data:
            institute.image = data["image"]

        for lang_code in ["az", "en"]:
            tr_payload = data.get(lang_code)
            if tr_payload:
                tr_q = await db.execute(select(ResearchInstituteTr).where(ResearchInstituteTr.institute_code == institute_code, ResearchInstituteTr.lang_code == lang_code))
                tr = tr_q.scalar_one_or_none()
                if tr:
                    for field in ["name", "about_html", "vision_html", "mission_html", "goals_html", "direction_html"]:
                        if field in tr_payload:
                            setattr(tr, field, tr_payload[field])
                    tr.updated_at = now
                else:
                    db.add(ResearchInstituteTr(
                        institute_code=institute_code,
                        lang_code=lang_code,
                        **tr_payload,
                        created_at=now,
                        updated_at=now,
                    ))

        if "director" in data:
            await _upsert_director(institute_code, data.get("director"), now, db)

        if "staff" in data:
            await db.execute(sqlalchemy_delete(InstituteStaff).where(InstituteStaff.institute_code == institute_code))
            if data["staff"]:
                await _create_staff(institute_code, data["staff"], now, db)

        institute.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Institute updated successfully.",
                "data": {"institute_code": institute.institute_code, "updated_at": institute.updated_at.isoformat()},
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_research_institute(institute_code: str, db: AsyncSession):
    try:
        inst_q = await db.execute(select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code))
        if not inst_q.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await db.execute(sqlalchemy_delete(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code))
        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Research Institute deleted successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_institute_image(institute_code: str, image: UploadFile, db: AsyncSession):
    try:
        inst_q = await db.execute(select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code))
        institute = inst_q.scalar_one_or_none()

        if not institute:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = institute.image
        new_path = await save_upload(image, "research-institutes", ALLOWED_IMAGE_MIMES)

        institute.image = new_path
        institute.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={"status_code": 200, "message": "Institute image uploaded successfully.", "data": {"image": new_path}},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_director_image(institute_code: str, image: UploadFile, db: AsyncSession):
    try:
        director_q = await db.execute(select(InstituteDirector).where(InstituteDirector.institute_code == institute_code))
        director = director_q.scalar_one_or_none()

        if not director:
            return JSONResponse(
                content={"status_code": 404, "message": "Director not found for this institute."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = director.image
        new_path = await save_upload(image, "institute-directors", ALLOWED_IMAGE_MIMES)

        director.image = new_path
        director.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={"status_code": 200, "message": "Director image uploaded successfully.", "data": {"image": new_path}},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_staff_image(staff_id: int, image: UploadFile, db: AsyncSession):
    try:
        member_q = await db.execute(select(InstituteStaff).where(InstituteStaff.id == staff_id))
        member = member_q.scalar_one_or_none()

        if not member:
            return JSONResponse(
                content={"status_code": 404, "message": "Staff member not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = member.image
        new_path = await save_upload(image, "institute-staff", ALLOWED_IMAGE_MIMES)

        member.image = new_path
        member.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={"status_code": 200, "message": "Staff member image uploaded successfully.", "data": {"image": new_path}},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
