import os
import random
from datetime import datetime
from sqlalchemy import select, func, delete as sqlalchemy_delete
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)

from app.api.v1.schema.collaboration import *
from fastapi import Depends, status, Query
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.models.collaboration.collaboration import Collaboration
from app.models.collaboration.collaboration_tr import CollaborationTranslation
from sqlalchemy.ext.asyncio import AsyncSession


def collaboration_id_generator():
    return random.randint(100000, 999999)


async def create_collaboration(
    request: CollaborationCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        collaboration_id = collaboration_id_generator()
        upload_dir = "app/static/collaborations/"
        os.makedirs(upload_dir, exist_ok=True)
        filename = request.logo.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{collaboration_id}.{ext}")
        file_content = await request.logo.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        logo_path = f"static/collaborations/{collaboration_id}.{ext}"

        result = await db.execute(select(Collaboration))
        existing = result.scalars().all()
        for item in existing:
            item.display_order = (item.display_order or 0) + 1
            db.add(item)
        display_order = 1

        new_collaboration = Collaboration(
            collaboration_id=collaboration_id,
            logo=logo_path,
            website_url=request.website_url,
            display_order=display_order,
            is_active=True,
            created_at=datetime.utcnow()
        )

        new_az = CollaborationTranslation(
            collaboration_id=collaboration_id,
            lang_code="az",
            name=request.az.name
        )

        new_en = CollaborationTranslation(
            collaboration_id=collaboration_id,
            lang_code="en",
            name=request.en.name
        )

        db.add(new_collaboration)
        db.add(new_az)
        db.add(new_en)
        await db.commit()
        await db.refresh(new_collaboration)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Collaboration created successfully."
            }, status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_collaborations(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Collaboration))
        total = total_query.scalar() or 0

        collab_query = await db.execute(
            select(Collaboration)
            .order_by(Collaboration.display_order.asc())
            .offset(start)
            .limit(end - start)
        )
        collaborations = collab_query.scalars().all()

        if not collaborations:
            return JSONResponse(
                content={
                    "status_code": 204,
                    "message": "No content."
                }, status_code=status.HTTP_204_NO_CONTENT
            )

        result_arr = []

        for collab in collaborations:
            tr_query = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collab.collaboration_id,
                    CollaborationTranslation.lang_code == lang
                )
            )
            translation = tr_query.scalar_one_or_none()

            result_arr.append({
                "id": collab.id,
                "collaboration_id": collab.collaboration_id,
                "logo": collab.logo,
                "website_url": collab.website_url,
                "display_order": collab.display_order,
                "name": translation.name if translation else None,
                "created_at": collab.created_at.isoformat() if collab.created_at else None
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaborations fetched successfully.",
                "total": total,
                "collaborations": result_arr
            }, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_collaboration_by_id(
    collaboration_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        collab_query = await db.execute(
            select(Collaboration).where(Collaboration.collaboration_id == collaboration_id)
        )
        collab = collab_query.scalar_one_or_none()

        if not collab:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Collaboration not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        tr_query = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.collaboration_id == collaboration_id,
                CollaborationTranslation.lang_code == lang
            )
        )
        translation = tr_query.scalar_one_or_none()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaboration fetched successfully.",
                "collaboration": {
                    "id": collab.id,
                    "collaboration_id": collab.collaboration_id,
                    "logo": collab.logo,
                    "website_url": collab.website_url,
                    "display_order": collab.display_order,
                    "name": translation.name if translation else None,
                    "created_at": collab.created_at.isoformat() if collab.created_at else None,
                    "updated_at": collab.updated_at.isoformat() if collab.updated_at else None
                }
            }, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def update_collaboration(
    collaboration_id: int,
    request: CollaborationUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab_query = await db.execute(
            select(Collaboration).where(Collaboration.collaboration_id == collaboration_id)
        )
        collab = collab_query.scalar_one_or_none()

        if not collab:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Collaboration not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        if request.logo and request.logo.filename:
            upload_dir = "app/static/collaborations/"
            os.makedirs(upload_dir, exist_ok=True)
            filename = request.logo.filename
            ext = filename.split(".")[-1]
            file_path = os.path.join(upload_dir, f"{collaboration_id}.{ext}")
            file_content = await request.logo.read()
            with open(file_path, "wb") as f:
                f.write(file_content)
            collab.logo = f"static/collaborations/{collaboration_id}.{ext}"

        if request.website_url is not None:
            collab.website_url = request.website_url

        db.add(collab)

        for lang_code, form in [("az", request.az), ("en", request.en)]:
            tr_query = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collaboration_id,
                    CollaborationTranslation.lang_code == lang_code
                )
            )
            translation = tr_query.scalar_one_or_none()
            if translation:
                translation.name = form.name
                db.add(translation)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaboration updated successfully."
            }, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def reorder_collaboration(
    request: ReOrderCollaboration,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Collaboration).where(Collaboration.collaboration_id == request.collaboration_id)
        )
        collab = result.scalar_one_or_none()

        if not collab:
            return JSONResponse(
                content={"status_code": 404, "error": "Collaboration not found"},
                status_code=404
            )

        old_order = collab.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(content={"status_code": 200, "message": "No change"}, status_code=200)

        if new_order < old_order:
            result = await db.execute(
                select(Collaboration).where(
                    Collaboration.display_order >= new_order,
                    Collaboration.display_order < old_order
                )
            )
            to_shift = result.scalars().all()
            for c in to_shift:
                c.display_order += 1
                db.add(c)
        else:
            result = await db.execute(
                select(Collaboration).where(
                    Collaboration.display_order <= new_order,
                    Collaboration.display_order > old_order
                )
            )
            to_shift = result.scalars().all()
            for c in to_shift:
                c.display_order -= 1
                db.add(c)

        collab.display_order = new_order
        db.add(collab)
        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Collaboration reordered successfully"},
            status_code=200
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=500
        )


async def delete_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        tr_stmt = sqlalchemy_delete(CollaborationTranslation).where(
            CollaborationTranslation.collaboration_id == collaboration_id
        )
        await db.execute(tr_stmt)

        stmt = sqlalchemy_delete(Collaboration).where(Collaboration.collaboration_id == collaboration_id)
        result = await db.execute(stmt)
        await db.commit()

        if result.rowcount == 0:
            return JSONResponse(
                content={"status_code": 404, "message": "Collaboration not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        return JSONResponse(
            content={"status_code": 200, "message": "Collaboration deleted successfully."},
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
