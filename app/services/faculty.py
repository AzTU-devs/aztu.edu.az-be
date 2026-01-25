import random
from datetime import datetime

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.models.faculties.faculties import Faculty
from app.models.faculties.faculties_tr import FacultyTr
from app.api.v1.schema.faculty import CreateFaculty, UpdateFaculty


def faculty_code_generator() -> str:
    return str(random.randint(100000, 999999))


async def create_faculty(
    request: CreateFaculty = Depends(CreateFaculty.as_form),
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

        faculty = Faculty(
            faculty_code=faculty_code,
            created_at=datetime.utcnow(),
        )

        faculty_tr_az = FacultyTr(
            faculty_code=faculty_code,
            lang_code="az",
            faculty_name=request.az.faculty_name,
            created_at=datetime.utcnow(),
        )

        faculty_tr_en = FacultyTr(
            faculty_code=faculty_code,
            lang_code="en",
            faculty_name=request.en.faculty_name,
            created_at=datetime.utcnow(),
        )

        db.add(faculty)
        db.add(faculty_tr_az)
        db.add(faculty_tr_en)

        await db.commit()
        await db.refresh(faculty)
        await db.refresh(faculty_tr_az)
        await db.refresh(faculty_tr_en)

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
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_faculties(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
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
                content={
                    "status_code": 204,
                    "message": "No content.",
                },
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

            faculties_arr.append(
                {
                    "id": faculty.id,
                    "faculty_code": faculty.faculty_code,
                    "faculty_name": tr.faculty_name if tr else None,
                    "created_at": faculty.created_at.isoformat()
                    if faculty.created_at
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
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e),
            },
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
                content={
                    "status_code": 404,
                    "message": "Faculty not found.",
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_query = await db.execute(
            select(FacultyTr).where(
                FacultyTr.faculty_code == faculty.faculty_code,
                FacultyTr.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()

        faculty_obj = {
            "id": faculty.id,
            "faculty_code": faculty.faculty_code,
            "faculty_name": tr.faculty_name if tr else None,
            "created_at": faculty.created_at.isoformat()
            if faculty.created_at
            else None,
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Faculty details fetched successfully.",
                "faculty": faculty_obj,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_faculty(
    faculty_code: str,
    request: UpdateFaculty = Depends(UpdateFaculty.as_form),
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == faculty_code)
        )
        faculty = faculty_query.scalar_one_or_none()

        if not faculty:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Faculty not found.",
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.az is None and request.en is None:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "message": "No fields to update.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.utcnow()

        async def upsert_translation(lang: str, name: str | None):
            if name is None:
                return
            tr_query = await db.execute(
                select(FacultyTr).where(
                    FacultyTr.faculty_code == faculty_code,
                    FacultyTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()
            if tr:
                tr.faculty_name = name
                tr.updated_at = now
            else:
                db.add(
                    FacultyTr(
                        faculty_code=faculty_code,
                        lang_code=lang,
                        faculty_name=name,
                        created_at=now,
                    )
                )

        await upsert_translation("az", request.az.faculty_name if request.az else None)
        await upsert_translation("en", request.en.faculty_name if request.en else None)

        faculty.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "faculty_code": faculty.faculty_code,
                    "faculty_name_az": request.az.faculty_name
                    if request.az
                    else None,
                    "faculty_name_en": request.en.faculty_name
                    if request.en
                    else None,
                    "updated_at": faculty.updated_at.isoformat()
                    if faculty.updated_at
                    else None,
                },
                "message": "Faculty updated successfully.",
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e),
            },
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
                content={
                    "status_code": 404,
                    "message": "Faculty not found.",
                },
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
            content={
                "status_code": 200,
                "message": "Faculty deleted successfully.",
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
