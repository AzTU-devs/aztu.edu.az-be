import random
from datetime import datetime

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.api.v1.schema.cafedra import CreateCafedra, UpdateCafedra
from app.models.faculties.faculties import Faculty
from app.models.cafedras.cafedras import Cafedra
from app.models.cafedras.cafedras_tr import CafedraTr


def cafedra_code_generator() -> str:
    return str(random.randint(100000, 999999))


async def create_cafedra(
    request: CreateCafedra = Depends(CreateCafedra.as_form),
    db: AsyncSession = Depends(get_db),
):
    try:
        faculty_query = await db.execute(
            select(Faculty).where(Faculty.faculty_code == request.faculty_code)
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

        cafedra_code = None
        for _ in range(10):
            candidate = cafedra_code_generator()
            existing_query = await db.execute(
                select(Cafedra).where(Cafedra.cafedra_code == candidate)
            )
            if not existing_query.scalar_one_or_none():
                cafedra_code = candidate
                break

        if not cafedra_code:
            return JSONResponse(
                content={
                    "status_code": 500,
                    "message": "Failed to generate unique cafedra code.",
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        now = datetime.utcnow()

        cafedra = Cafedra(
            faculty_code=request.faculty_code,
            cafedra_code=cafedra_code,
            created_at=now,
        )

        cafedra_tr_az = CafedraTr(
            cafedra_code=cafedra_code,
            lang_code="az",
            cafedra_name=request.az.cafedra_name,
            created_at=now,
        )

        cafedra_tr_en = CafedraTr(
            cafedra_code=cafedra_code,
            lang_code="en",
            cafedra_name=request.en.cafedra_name,
            created_at=now,
        )

        db.add(cafedra)
        db.add(cafedra_tr_az)
        db.add(cafedra_tr_en)

        await db.commit()
        await db.refresh(cafedra)

        return JSONResponse(
            content={
                "status_code": 201,
                "data": {
                    "cafedra_code": cafedra.cafedra_code,
                    "faculty_code": cafedra.faculty_code,
                    "cafedra_name_az": request.az.cafedra_name,
                    "cafedra_name_en": request.en.cafedra_name,
                    "created_at": cafedra.created_at.isoformat()
                },
                "message": "Cafedra created successfully.",
            },
            status_code=status.HTTP_201_CREATED,
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


async def get_cafedras(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Cafedra))
        total = total_query.scalar() or 0

        query = select(Cafedra).order_by(Cafedra.id.asc()).offset(start).limit(end - start)
        if faculty_code:
            query = query.where(Cafedra.faculty_code == faculty_code)

        cafedra_query = await db.execute(query)
        cafedras = cafedra_query.scalars().all()

        if not cafedras:
            return JSONResponse(
                content={
                    "status_code": 204,
                    "message": "No content.",
                },
                status_code=status.HTTP_204_NO_CONTENT,
            )

        cafedras_arr = []
        for cafedra in cafedras:
            tr_query = await db.execute(
                select(CafedraTr).where(
                    CafedraTr.cafedra_code == cafedra.cafedra_code,
                    CafedraTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()

            cafedras_arr.append(
                {
                    "id": cafedra.id,
                    "faculty_code": cafedra.faculty_code,
                    "cafedra_code": cafedra.cafedra_code,
                    "cafedra_name": tr.cafedra_name if tr else None,
                    "created_at": cafedra.created_at.isoformat()
                    if cafedra.created_at
                    else None,
                }
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Cafedras fetched successfully.",
                "cafedras": cafedras_arr,
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


async def get_cafedra(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        cafedra_query = await db.execute(
            select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
        )
        cafedra = cafedra_query.scalar_one_or_none()

        if not cafedra:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Cafedra not found.",
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_query = await db.execute(
            select(CafedraTr).where(
                CafedraTr.cafedra_code == cafedra.cafedra_code,
                CafedraTr.lang_code == lang_code,
            )
        )
        tr = tr_query.scalar_one_or_none()

        cafedra_obj = {
            "id": cafedra.id,
            "faculty_code": cafedra.faculty_code,
            "cafedra_code": cafedra.cafedra_code,
            "cafedra_name": tr.cafedra_name if tr else None,
            "created_at": cafedra.created_at.isoformat()
            if cafedra.created_at
            else None,
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Cafedra details fetched successfully.",
                "cafedra": cafedra_obj,
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


async def update_cafedra(
    cafedra_code: str,
    request: UpdateCafedra = Depends(UpdateCafedra.as_form),
    db: AsyncSession = Depends(get_db),
):
    try:
        cafedra_query = await db.execute(
            select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
        )
        cafedra = cafedra_query.scalar_one_or_none()

        if not cafedra:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Cafedra not found.",
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
                select(CafedraTr).where(
                    CafedraTr.cafedra_code == cafedra_code,
                    CafedraTr.lang_code == lang,
                )
            )
            tr = tr_query.scalar_one_or_none()
            if tr:
                tr.cafedra_name = name
                tr.updated_at = now
            else:
                db.add(
                    CafedraTr(
                        cafedra_code=cafedra_code,
                        lang_code=lang,
                        cafedra_name=name,
                        created_at=now,
                    )
                )

        await upsert_translation("az", request.az.cafedra_name if request.az else None)
        await upsert_translation("en", request.en.cafedra_name if request.en else None)

        cafedra.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "cafedra_code": cafedra.cafedra_code,
                    "faculty_code": cafedra.faculty_code,
                    "cafedra_name_az": request.az.cafedra_name
                    if request.az
                    else None,
                    "cafedra_name_en": request.en.cafedra_name
                    if request.en
                    else None,
                    "updated_at": cafedra.updated_at.isoformat() if cafedra.updated_at else None,
                },
                "message": "Cafedra updated successfully.",
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


async def delete_cafedra(
    cafedra_code: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        cafedra_query = await db.execute(
            select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
        )
        cafedra = cafedra_query.scalar_one_or_none()

        if not cafedra:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Cafedra not found.",
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await db.execute(
            sqlalchemy_delete(CafedraTr).where(CafedraTr.cafedra_code == cafedra_code)
        )
        await db.execute(
            sqlalchemy_delete(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
        )

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Cafedra deleted successfully.",
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
