import secrets
from datetime import datetime, timezone
from typing import Any, Type

from fastapi import Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.research_institute import (
    CreateResearchInstitute,
    UpdateResearchInstitute,
)
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload
from app.core.logger import get_logger
from app.core.session import get_db
from app.models.research_institutes.research_institute import ResearchInstitute, ResearchInstituteTr
from app.models.research_institutes.institute_details import (
    InstituteObjective,
    InstituteObjectiveTr,
    InstituteResearchDirection,
    InstituteResearchDirectionTr,
)
from app.models.research_institutes.institute_people import (
    InstituteDirector,
    InstituteDirectorTr,
    DirectorResearchArea,
    DirectorResearchAreaTr,
    InstituteDirectorEducation,
    InstituteDirectorEducationTr,
    InstituteStaff,
    InstituteStaffTr,
)
from app.utils.language import get_language

logger = get_logger(__name__)


async def create_research_institute(
    request: CreateResearchInstitute,
    db: AsyncSession,
):
    try:
        now = datetime.now(timezone.utc)
        
        # Check if institute_code already exists
        existing_q = await db.execute(
            select(ResearchInstitute).where(ResearchInstitute.institute_code == request.institute_code)
        )
        if existing_q.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 400, "message": f"Institute code '{request.institute_code}' already exists."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        institute = ResearchInstitute(
            institute_code=request.institute_code,
            image_url=request.image_url,
            created_at=now,
            updated_at=now,
        )
        db.add(institute)
        await db.flush()

        # Translations
        db.add(ResearchInstituteTr(
            institute_code=institute.institute_code,
            lang_code="az",
            name=request.az.name,
            about=request.az.about,
            vision=request.az.vision,
            mission=request.az.mission,
            created_at=now,
            updated_at=now,
        ))
        db.add(ResearchInstituteTr(
            institute_code=institute.institute_code,
            lang_code="en",
            name=request.en.name,
            about=request.en.about,
            vision=request.en.vision,
            mission=request.en.mission,
            created_at=now,
            updated_at=now,
        ))

        # Director
        if request.director:
            director = InstituteDirector(
                institute_code=institute.institute_code,
                full_name=request.director.full_name,
                email=request.director.email,
                office=request.director.office,
                image_url=request.director.image_url,
                created_at=now,
                updated_at=now,
            )
            db.add(director)
            await db.flush()

            db.add(InstituteDirectorTr(
                director_id=director.id,
                lang_code="az",
                title=request.director.az.title,
                biography=request.director.az.biography,
                created_at=now,
                updated_at=now,
            ))
            db.add(InstituteDirectorTr(
                director_id=director.id,
                lang_code="en",
                title=request.director.en.title,
                biography=request.director.en.biography,
                created_at=now,
                updated_at=now,
            ))

            if request.director.research_areas:
                for index, ra in enumerate(request.director.research_areas):
                    area = DirectorResearchArea(
                        director_id=director.id,
                        display_order=index,
                        created_at=now,
                        updated_at=now,
                    )
                    db.add(area)
                    await db.flush()
                    db.add(DirectorResearchAreaTr(
                        research_area_id=area.id,
                        lang_code="az",
                        content=ra.az.content,
                        created_at=now,
                        updated_at=now,
                    ))
                    db.add(DirectorResearchAreaTr(
                        research_area_id=area.id,
                        lang_code="en",
                        content=ra.en.content,
                        created_at=now,
                        updated_at=now,
                    ))

            if request.director.educations:
                for index, edu in enumerate(request.director.educations):
                    education = InstituteDirectorEducation(
                        director_id=director.id,
                        start_year=edu.start_year,
                        end_year=edu.end_year,
                        display_order=index,
                        created_at=now,
                        updated_at=now,
                    )
                    db.add(education)
                    await db.flush()
                    db.add(InstituteDirectorEducationTr(
                        education_id=education.id,
                        lang_code="az",
                        university=edu.az.university,
                        degree=edu.az.degree,
                        created_at=now,
                        updated_at=now,
                    ))
                    db.add(InstituteDirectorEducationTr(
                        education_id=education.id,
                        lang_code="en",
                        university=edu.en.university,
                        degree=edu.en.degree,
                        created_at=now,
                        updated_at=now,
                    ))

        # Objectives
        if request.objectives:
            for index, obj in enumerate(request.objectives):
                objective = InstituteObjective(
                    institute_code=institute.institute_code,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(objective)
                await db.flush()
                db.add(InstituteObjectiveTr(
                    objective_id=objective.id,
                    lang_code="az",
                    content=obj.az.content,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteObjectiveTr(
                    objective_id=objective.id,
                    lang_code="en",
                    content=obj.en.content,
                    created_at=now,
                    updated_at=now,
                ))

        # Research Directions
        if request.research_directions:
            for index, rd in enumerate(request.research_directions):
                direction = InstituteResearchDirection(
                    institute_code=institute.institute_code,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(direction)
                await db.flush()
                db.add(InstituteResearchDirectionTr(
                    research_direction_id=direction.id,
                    lang_code="az",
                    content=rd.az.content,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteResearchDirectionTr(
                    research_direction_id=direction.id,
                    lang_code="en",
                    content=rd.en.content,
                    created_at=now,
                    updated_at=now,
                ))

        # Staff
        if request.staff:
            for index, st in enumerate(request.staff):
                staff = InstituteStaff(
                    institute_code=institute.institute_code,
                    full_name=st.full_name,
                    email=st.email,
                    phone=st.phone,
                    image_url=st.image_url,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(staff)
                await db.flush()
                db.add(InstituteStaffTr(
                    staff_id=staff.id,
                    lang_code="az",
                    title=st.az.title,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteStaffTr(
                    staff_id=staff.id,
                    lang_code="en",
                    title=st.en.title,
                    created_at=now,
                    updated_at=now,
                ))

        await db.commit()
        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Research Institute created successfully.",
                "data": {"institute_code": institute.institute_code},
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("Error creating research institute")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_institutes(
    start: int = 0,
    end: int = 10,
    lang: str = "az",
    db: AsyncSession = None,
):
    try:
        total_q = await db.execute(select(func.count()).select_from(ResearchInstitute))
        total = total_q.scalar() or 0

        query = await db.execute(
            select(ResearchInstitute)
            .order_by(ResearchInstitute.created_at.desc())
            .offset(start)
            .limit(end - start)
        )
        institutes = query.scalars().all()

        result = []
        for inst in institutes:
            tr_q = await db.execute(
                select(ResearchInstituteTr).where(
                    ResearchInstituteTr.institute_code == inst.institute_code,
                    ResearchInstituteTr.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()
            result.append({
                "id": inst.id,
                "institute_code": inst.institute_code,
                "image_url": inst.image_url,
                "name": tr.name if tr else None,
                "about": tr.about if tr else None,
                "created_at": inst.created_at.isoformat(),
                "updated_at": inst.updated_at.isoformat() if inst.updated_at else None,
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Institutes fetched successfully.",
                "data": result,
                "total": total,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error fetching research institutes")
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_institute(
    institute_code: str,
    lang: str = "az",
    db: AsyncSession = None,
):
    try:
        inst_q = await db.execute(
            select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code)
        )
        inst = inst_q.scalar_one_or_none()
        if not inst:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(ResearchInstituteTr).where(
                ResearchInstituteTr.institute_code == institute_code,
                ResearchInstituteTr.lang_code == lang,
            )
        )
        tr = tr_q.scalar_one_or_none()

        # Director
        director_q = await db.execute(
            select(InstituteDirector).where(InstituteDirector.institute_code == institute_code)
        )
        director = director_q.scalar_one_or_none()
        director_data = None
        if director:
            dir_tr_q = await db.execute(
                select(InstituteDirectorTr).where(
                    InstituteDirectorTr.director_id == director.id,
                    InstituteDirectorTr.lang_code == lang,
                )
            )
            dir_tr = dir_tr_q.scalar_one_or_none()

            ra_q = await db.execute(
                select(DirectorResearchArea).where(DirectorResearchArea.director_id == director.id).order_by(DirectorResearchArea.display_order.asc())
            )
            areas = []
            for ra in ra_q.scalars().all():
                ra_tr_q = await db.execute(
                    select(DirectorResearchAreaTr).where(
                        DirectorResearchAreaTr.research_area_id == ra.id,
                        DirectorResearchAreaTr.lang_code == lang,
                    )
                )
                ra_tr = ra_tr_q.scalar_one_or_none()
                areas.append({"id": ra.id, "content": ra_tr.content if ra_tr else None})

            edu_q = await db.execute(
                select(InstituteDirectorEducation).where(InstituteDirectorEducation.director_id == director.id).order_by(InstituteDirectorEducation.display_order.asc())
            )
            educations = []
            for edu in edu_q.scalars().all():
                edu_tr_q = await db.execute(
                    select(InstituteDirectorEducationTr).where(
                        InstituteDirectorEducationTr.education_id == edu.id,
                        InstituteDirectorEducationTr.lang_code == lang,
                    )
                )
                edu_tr = edu_tr_q.scalar_one_or_none()
                educations.append({
                    "id": edu.id,
                    "university": edu_tr.university if edu_tr else None,
                    "degree": edu_tr.degree if edu_tr else None,
                    "start_year": edu.start_year,
                    "end_year": edu.end_year,
                })

            director_data = {
                "id": director.id,
                "full_name": director.full_name,
                "email": director.email,
                "office": director.office,
                "image_url": director.image_url,
                "title": dir_tr.title if dir_tr else None,
                "biography": dir_tr.biography if dir_tr else None,
                "research_areas": areas,
                "educations": educations,
            }

        # Objectives
        obj_q = await db.execute(
            select(InstituteObjective).where(InstituteObjective.institute_code == institute_code).order_by(InstituteObjective.display_order.asc())
        )
        objectives = []
        for obj in obj_q.scalars().all():
            obj_tr_q = await db.execute(
                select(InstituteObjectiveTr).where(
                    InstituteObjectiveTr.objective_id == obj.id,
                    InstituteObjectiveTr.lang_code == lang,
                )
            )
            obj_tr = obj_tr_q.scalar_one_or_none()
            objectives.append({"id": obj.id, "content": obj_tr.content if obj_tr else None})

        # Research Directions
        rd_q = await db.execute(
            select(InstituteResearchDirection).where(InstituteResearchDirection.institute_code == institute_code).order_by(InstituteResearchDirection.display_order.asc())
        )
        directions = []
        for rd in rd_q.scalars().all():
            rd_tr_q = await db.execute(
                select(InstituteResearchDirectionTr).where(
                    InstituteResearchDirectionTr.research_direction_id == rd.id,
                    InstituteResearchDirectionTr.lang_code == lang,
                )
            )
            rd_tr = rd_tr_q.scalar_one_or_none()
            directions.append({"id": rd.id, "content": rd_tr.content if rd_tr else None})

        # Staff
        st_q = await db.execute(
            select(InstituteStaff).where(InstituteStaff.institute_code == institute_code).order_by(InstituteStaff.display_order.asc())
        )
        staff_list = []
        for st in st_q.scalars().all():
            st_tr_q = await db.execute(
                select(InstituteStaffTr).where(
                    InstituteStaffTr.staff_id == st.id,
                    InstituteStaffTr.lang_code == lang,
                )
            )
            st_tr = st_tr_q.scalar_one_or_none()
            staff_list.append({
                "id": st.id,
                "full_name": st.full_name,
                "email": st.email,
                "phone": st.phone,
                "image_url": st.image_url,
                "title": st_tr.title if st_tr else None,
            })

        result = {
            "id": inst.id,
            "institute_code": inst.institute_code,
            "image_url": inst.image_url,
            "name": tr.name if tr else None,
            "about": tr.about if tr else None,
            "vision": tr.vision if tr else None,
            "mission": tr.mission if tr else None,
            "director": director_data,
            "objectives": objectives,
            "research_directions": directions,
            "staff": staff_list,
            "created_at": inst.created_at.isoformat(),
            "updated_at": inst.updated_at.isoformat() if inst.updated_at else None,
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Institute details fetched successfully.",
                "data": result,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error fetching research institute details")
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_research_institute(
    institute_code: str,
    request: UpdateResearchInstitute,
    db: AsyncSession,
):
    try:
        inst_q = await db.execute(
            select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code)
        )
        inst = inst_q.scalar_one_or_none()
        if not inst:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        now = datetime.now(timezone.utc)
        if request.image_url is not None:
            inst.image_url = request.image_url

        # Translations
        for lang, translation in [("az", request.az), ("en", request.en)]:
            if translation:
                tr_q = await db.execute(
                    select(ResearchInstituteTr).where(
                        ResearchInstituteTr.institute_code == institute_code,
                        ResearchInstituteTr.lang_code == lang,
                    )
                )
                tr = tr_q.scalar_one_or_none()
                if tr:
                    if translation.name: tr.name = translation.name
                    if translation.about: tr.about = translation.about
                    if translation.vision: tr.vision = translation.vision
                    if translation.mission: tr.mission = translation.mission
                    tr.updated_at = now
                else:
                    db.add(ResearchInstituteTr(
                        institute_code=institute_code,
                        lang_code=lang,
                        name=translation.name,
                        about=translation.about,
                        vision=translation.vision,
                        mission=translation.mission,
                        created_at=now,
                        updated_at=now,
                    ))

        # Re-creating sub-entities for simplicity in this implementation
        # (similar to how faculty update handles some sections)
        
        if request.director:
            await db.execute(sqlalchemy_delete(InstituteDirector).where(InstituteDirector.institute_code == institute_code))
            # (Note: Cascade will handle translations and research areas)
            director = InstituteDirector(
                institute_code=institute_code,
                full_name=request.director.full_name,
                email=request.director.email,
                office=request.director.office,
                image_url=request.director.image_url,
                created_at=now,
                updated_at=now,
            )
            db.add(director)
            await db.flush()

            db.add(InstituteDirectorTr(
                director_id=director.id,
                lang_code="az",
                title=request.director.az.title,
                biography=request.director.az.biography,
                created_at=now,
                updated_at=now,
            ))
            db.add(InstituteDirectorTr(
                director_id=director.id,
                lang_code="en",
                title=request.director.en.title,
                biography=request.director.en.biography,
                created_at=now,
                updated_at=now,
            ))

            if request.director.research_areas:
                for index, ra in enumerate(request.director.research_areas):
                    area = DirectorResearchArea(
                        director_id=director.id,
                        display_order=index,
                        created_at=now,
                        updated_at=now,
                    )
                    db.add(area)
                    await db.flush()
                    db.add(DirectorResearchAreaTr(
                        research_area_id=area.id,
                        lang_code="az",
                        content=ra.az.content,
                        created_at=now,
                        updated_at=now,
                    ))
                    db.add(DirectorResearchAreaTr(
                        research_area_id=area.id,
                        lang_code="en",
                        content=ra.en.content,
                        created_at=now,
                        updated_at=now,
                    ))

            if request.director.educations:
                for index, edu in enumerate(request.director.educations):
                    education = InstituteDirectorEducation(
                        director_id=director.id,
                        start_year=edu.start_year,
                        end_year=edu.end_year,
                        display_order=index,
                        created_at=now,
                        updated_at=now,
                    )
                    db.add(education)
                    await db.flush()
                    db.add(InstituteDirectorEducationTr(
                        education_id=education.id,
                        lang_code="az",
                        university=edu.az.university,
                        degree=edu.az.degree,
                        created_at=now,
                        updated_at=now,
                    ))
                    db.add(InstituteDirectorEducationTr(
                        education_id=education.id,
                        lang_code="en",
                        university=edu.en.university,
                        degree=edu.en.degree,
                        created_at=now,
                        updated_at=now,
                    ))

        if request.objectives is not None:
            await db.execute(sqlalchemy_delete(InstituteObjective).where(InstituteObjective.institute_code == institute_code))
            for index, obj in enumerate(request.objectives):
                objective = InstituteObjective(
                    institute_code=institute_code,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(objective)
                await db.flush()
                db.add(InstituteObjectiveTr(
                    objective_id=objective.id,
                    lang_code="az",
                    content=obj.az.content,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteObjectiveTr(
                    objective_id=objective.id,
                    lang_code="en",
                    content=obj.en.content,
                    created_at=now,
                    updated_at=now,
                ))

        if request.research_directions is not None:
            await db.execute(sqlalchemy_delete(InstituteResearchDirection).where(InstituteResearchDirection.institute_code == institute_code))
            for index, rd in enumerate(request.research_directions):
                direction = InstituteResearchDirection(
                    institute_code=institute_code,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(direction)
                await db.flush()
                db.add(InstituteResearchDirectionTr(
                    research_direction_id=direction.id,
                    lang_code="az",
                    content=rd.az.content,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteResearchDirectionTr(
                    research_direction_id=direction.id,
                    lang_code="en",
                    content=rd.en.content,
                    created_at=now,
                    updated_at=now,
                ))

        if request.staff is not None:
            await db.execute(sqlalchemy_delete(InstituteStaff).where(InstituteStaff.institute_code == institute_code))
            for index, st in enumerate(request.staff):
                staff = InstituteStaff(
                    institute_code=institute_code,
                    full_name=st.full_name,
                    email=st.email,
                    phone=st.phone,
                    image_url=st.image_url,
                    display_order=index,
                    created_at=now,
                    updated_at=now,
                )
                db.add(staff)
                await db.flush()
                db.add(InstituteStaffTr(
                    staff_id=staff.id,
                    lang_code="az",
                    title=st.az.title,
                    created_at=now,
                    updated_at=now,
                ))
                db.add(InstituteStaffTr(
                    staff_id=staff.id,
                    lang_code="en",
                    title=st.en.title,
                    created_at=now,
                    updated_at=now,
                ))

        inst.updated_at = now
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Research Institute updated successfully."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error updating research institute")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_research_institute(
    institute_code: str,
    db: AsyncSession,
):
    try:
        inst_q = await db.execute(
            select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code)
        )
        inst = inst_q.scalar_one_or_none()
        if not inst:
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
    except Exception as e:
        logger.exception("Error deleting research institute")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_institute_image(
    institute_code: str,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        inst_q = await db.execute(
            select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code)
        )
        inst = inst_q.scalar_one_or_none()
        if not inst:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Institute not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = inst.image_url
        new_path = await save_upload(image, "research_institutes", ALLOWED_IMAGE_MIMES)

        inst.image_url = new_path
        inst.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Institute image uploaded successfully.",
                "data": {"image_url": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error uploading institute image")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_director_image(
    director_id: int,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        dir_q = await db.execute(
            select(InstituteDirector).where(InstituteDirector.id == director_id)
        )
        director = dir_q.scalar_one_or_none()
        if not director:
            return JSONResponse(
                content={"status_code": 404, "message": "Director not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = director.image_url
        new_path = await save_upload(image, "institute_directors", ALLOWED_IMAGE_MIMES)

        director.image_url = new_path
        director.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Director image uploaded successfully.",
                "data": {"image_url": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error uploading director image")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_staff_image(
    staff_id: int,
    image: UploadFile,
    db: AsyncSession,
):
    try:
        st_q = await db.execute(
            select(InstituteStaff).where(InstituteStaff.id == staff_id)
        )
        staff = st_q.scalar_one_or_none()
        if not staff:
            return JSONResponse(
                content={"status_code": 404, "message": "Staff member not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = staff.image_url
        new_path = await save_upload(image, "institute_staff", ALLOWED_IMAGE_MIMES)

        staff.image_url = new_path
        staff.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Staff image uploaded successfully.",
                "data": {"image_url": new_path},
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("Error uploading staff image")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
