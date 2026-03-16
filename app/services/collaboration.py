import secrets
from datetime import datetime, timezone
from sqlalchemy import select, func, delete as sqlalchemy_delete
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)

from app.api.v1.schema.collaboration import *
from fastapi import Depends, status, Query
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.models.collaboration.collaboration import Collaboration
from app.models.collaboration.collaboration_tr import CollaborationTranslation
from sqlalchemy.ext.asyncio import AsyncSession


def collaboration_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


async def create_collaboration(
    request: CollaborationCreate,
    db: AsyncSession = Depends(get_db),
):
    saved_files: list[str] = []
    try:
        collaboration_id = collaboration_id_generator()

        logo_path = await save_upload(request.logo, "collaborations", ALLOWED_IMAGE_MIMES)
        saved_files.append(logo_path)

        for item in (await db.execute(select(Collaboration))).scalars().all():
            item.display_order = (item.display_order or 0) + 1
            db.add(item)

        db.add(Collaboration(
            collaboration_id=collaboration_id,
            logo=logo_path,
            website_url=request.website_url,
            display_order=1,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        ))
        db.add(CollaborationTranslation(collaboration_id=collaboration_id, lang_code="az", name=request.az.name))
        db.add(CollaborationTranslation(collaboration_id=collaboration_id, lang_code="en", name=request.en.name))
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Collaboration created successfully."},
            status_code=status.HTTP_201_CREATED
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create collaboration")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_collaborations(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0, le=100),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(Collaboration))).scalar() or 0
        collaborations = (await db.execute(
            select(Collaboration).order_by(Collaboration.display_order.asc()).offset(start).limit(end - start)
        )).scalars().all()

        if not collaborations:
            return JSONResponse(content={"status_code": 204, "message": "No content."}, status_code=status.HTTP_204_NO_CONTENT)

        result_arr = []
        for collab in collaborations:
            tr = (await db.execute(
                select(CollaborationTranslation).where(
                    CollaborationTranslation.collaboration_id == collab.collaboration_id,
                    CollaborationTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            result_arr.append({
                "id": collab.id,
                "collaboration_id": collab.collaboration_id,
                "logo": collab.logo,
                "website_url": collab.website_url,
                "display_order": collab.display_order,
                "name": tr.name if tr else None,
                "created_at": collab.created_at.isoformat() if collab.created_at else None,
            })

        return JSONResponse(content={"status_code": 200, "message": "Collaborations fetched successfully.", "total": total, "collaborations": result_arr})

    except Exception:
        logger.exception("Failed to fetch collaborations")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_collaboration_by_id(
    collaboration_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        collab = (await db.execute(select(Collaboration).where(Collaboration.collaboration_id == collaboration_id))).scalar_one_or_none()
        if not collab:
            return JSONResponse(content={"status_code": 404, "message": "Collaboration not found."}, status_code=status.HTTP_404_NOT_FOUND)

        tr = (await db.execute(
            select(CollaborationTranslation).where(
                CollaborationTranslation.collaboration_id == collaboration_id,
                CollaborationTranslation.lang_code == lang
            )
        )).scalar_one_or_none()

        return JSONResponse(content={
            "status_code": 200,
            "message": "Collaboration fetched successfully.",
            "collaboration": {
                "id": collab.id,
                "collaboration_id": collab.collaboration_id,
                "logo": collab.logo,
                "website_url": collab.website_url,
                "display_order": collab.display_order,
                "name": tr.name if tr else None,
                "created_at": collab.created_at.isoformat() if collab.created_at else None,
                "updated_at": collab.updated_at.isoformat() if collab.updated_at else None,
            }
        })

    except Exception:
        logger.exception("Failed to fetch collaboration by id")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_collaboration(
    collaboration_id: int,
    request: CollaborationUpdate,
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []
    try:
        collab = (await db.execute(select(Collaboration).where(Collaboration.collaboration_id == collaboration_id))).scalar_one_or_none()
        if not collab:
            return JSONResponse(content={"status_code": 404, "message": "Collaboration not found."}, status_code=status.HTTP_404_NOT_FOUND)

        old_logo = collab.logo

        if request.logo and request.logo.filename:
            new_logo_path = await save_upload(request.logo, "collaborations", ALLOWED_IMAGE_MIMES)
            saved_files.append(new_logo_path)
            collab.logo = new_logo_path

        if request.website_url is not None:
            collab.website_url = request.website_url

        db.add(collab)

        for lang_code, form in [("az", request.az), ("en", request.en)]:
            tr = (await db.execute(
                select(CollaborationTranslation).where(
                    CollaborationTranslation.collaboration_id == collaboration_id,
                    CollaborationTranslation.lang_code == lang_code
                )
            )).scalar_one_or_none()
            if tr:
                tr.name = form.name
                db.add(tr)

        await db.commit()

        # Delete old logo only after successful commit
        if saved_files and old_logo:
            safe_delete_file(old_logo)

        return JSONResponse(content={"status_code": 200, "message": "Collaboration updated successfully."})

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to update collaboration")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def reorder_collaboration(
    request: ReOrderCollaboration,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab = (await db.execute(select(Collaboration).where(Collaboration.collaboration_id == request.collaboration_id))).scalar_one_or_none()
        if not collab:
            return JSONResponse(content={"status_code": 404, "error": "Collaboration not found"}, status_code=404)

        old_order = collab.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(content={"status_code": 200, "message": "No change"})

        if new_order < old_order:
            rows = (await db.execute(select(Collaboration).where(Collaboration.display_order >= new_order, Collaboration.display_order < old_order))).scalars().all()
            for r in rows:
                r.display_order += 1
                db.add(r)
        else:
            rows = (await db.execute(select(Collaboration).where(Collaboration.display_order <= new_order, Collaboration.display_order > old_order))).scalars().all()
            for r in rows:
                r.display_order -= 1
                db.add(r)

        collab.display_order = new_order
        db.add(collab)
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Collaboration reordered successfully"})

    except Exception:
        logger.exception("Failed to reorder collaboration")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)


async def delete_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab = (await db.execute(select(Collaboration).where(Collaboration.collaboration_id == collaboration_id))).scalar_one_or_none()
        if not collab:
            return JSONResponse(content={"status_code": 404, "message": "Collaboration not found."}, status_code=status.HTTP_404_NOT_FOUND)

        logo_path = collab.logo

        await db.execute(sqlalchemy_delete(CollaborationTranslation).where(CollaborationTranslation.collaboration_id == collaboration_id))
        await db.execute(sqlalchemy_delete(Collaboration).where(Collaboration.collaboration_id == collaboration_id))
        await db.commit()

        safe_delete_file(logo_path)

        return JSONResponse(content={"status_code": 200, "message": "Collaboration deleted successfully."})

    except Exception:
        logger.exception("Failed to delete collaboration")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
