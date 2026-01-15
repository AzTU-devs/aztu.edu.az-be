import os
import random
from typing import Optional
from datetime import datetime
from sqlalchemy import select, func
from app.core.database import get_db
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.collabortion import *
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.collaboration.collaboration import Collaboration
from fastapi import UploadFile, File, Form, Depends, Query, status
from app.models.collaboration.collaboration_translation import CollaborationTranslation

def collaboration_id_generator():
    return random.randint(100000, 999999)

async def create_collaboration(
    image: UploadFile = File(...),
    az_title: str = Form(...),
    en_title: str = Form(...),
    url: Optional[str] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    collaboration_id = collaboration_id_generator()
    upload_dir = "app/static/collaborations/"
    os.makedirs(upload_dir, exist_ok=True)
    filename = image.filename
    ext = filename.split(".")[-1]
    file_path = os.path.join(upload_dir, f"{collaboration_id}.{ext}")
    file_content = await image.read()
    with open(file_path, "wb") as f:
        f.write(file_content)

    image_path = f"static/collaborations/{collaboration_id}.{ext}"

    try:
        collab_query_az = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.title == az_title,
                CollaborationTranslation.lang_code == "az"
            )
        )

        collab_az = collab_query_az.scalar_one_or_none()

        collab_query_en = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.title == az_title,
                CollaborationTranslation.lang_code == "en"
            )
        )

        collab_en = collab_query_en.scalar_one_or_none()

        if collab_az or collab_en:
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Title already exists."
                }, status_code=status.HTTP_409_CONFLICT
            )

        try:
            result = await db.execute(select(Collaboration))
            existing_announcements = result.scalars().all()
            for announcement in existing_announcements:
                announcement.display_order = (announcement.display_order or 0) + 1
                db.add(announcement)
            display_order = 1
        except UndefinedTableError:
            display_order = 1
        
        new_collaboration = Collaboration(
            collaboration_id=collaboration_id,
            display_order=display_order,
            image=image_path,
            url = url,
            is_active=True,
            created_at=datetime.utcnow()
        )

        new_collaboration_az = CollaborationTranslation(
            collaboration_id=collaboration_id,
            lang_code="az",
            title=az_title
        )

        new_collaboration_en = CollaborationTranslation(
            collaboration_id=collaboration_id,
            lang_code="en",
            title=en_title
        )

        db.add(new_collaboration)
        db.add(new_collaboration_az)
        db.add(new_collaboration_en)

        await db.commit()

        await db.refresh(new_collaboration)
        await db.refresh(new_collaboration_az)
        await db.refresh(new_collaboration_en)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Collaboration created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_collaborations(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
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
            .where(Collaboration.is_active == True)
        )

        collabs = collab_query.scalars().all()

        if not collabs:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        collaborations_arr = []


        for collaboration in collabs:
            translation_query = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collaboration.collaboration_id,
                    CollaborationTranslation.lang_code == lang
                )
            )

            collab_tr = translation_query.scalar_one_or_none()

            collab_obj = {
                "title": collab_tr.title,
                "display_order": collaboration.display_order,
                "url": collaboration.url,
                "image": collaboration.image,
                "created_at": collaboration.created_at.isoformat() if collaboration.created_at else None,
                "updated_at": collaboration.updated_at.isoformat() if collaboration.updated_at else None
            }        

            collaborations_arr.append(collab_obj)
            
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaborations fetched successfully.",
                "collaborations": collaborations_arr,
                "total": total
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def deactivate_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab_query = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == collaboration_id)
        )

        collaboration = collab_query.scalar_one_or_none()

        if not collaboration:
            return JSONResponse(
                content={
                    "status_code": 404
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        collaboration.is_active = False

        await db.commit()
        await db.refresh(collaboration)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaboration deactivated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def activate_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab_query = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == collaboration_id)
        )

        collaboration = collab_query.scalar_one_or_none()

        if not collaboration:
            return JSONResponse(
                content={
                    "status_code": 404
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        collaboration.is_active = True

        await db.commit()
        await db.refresh(collaboration)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaboration activated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def delete_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        collab_query = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == collaboration_id)
        )

        collaboration = collab_query.scalar_one_or_none()

        if not collaboration:
            return JSONResponse(
                content={
                    "status_code": 404
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        collab_tr_az_query = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.collaboration_id == collaboration_id,
                CollaborationTranslation.lang_code == "az"
            )
        )

        collab_tr_az = collab_tr_az_query.scalar_one_or_none()
        
        collab_tr_en_query = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.collaboration_id == collaboration_id,
                CollaborationTranslation.lang_code == "en"
            )
        )

        collab_tr_en = collab_tr_en_query.scalar_one_or_none()

        await db.delete(collaboration)
        await db.delete(collab_tr_az)
        await db.delete(collab_tr_en)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaboration deleted successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
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
        collab_query = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == request.collaboration_id)
        )

        collaboration = collab_query.scalar_one_or_none()

        if not collaboration:
            return JSONResponse(
                content={
                    "status_code": 404
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        old_order = collaboration.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(
                content={
                    "status_code": 200,
                    "message": "No change"
                }, status_code=200)

        if new_order < old_order:
            result = await db.execute(
                select(Collaboration).where(
                    Collaboration.display_order >= new_order,
                    Collaboration.display_order < old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order += 1
                db.add(p)
        else:
            result = await db.execute(
                select(Collaboration).where(
                    Collaboration.display_order <= new_order,
                    Collaboration.display_order > old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order -= 1
                db.add(p)

        collaboration.display_order = new_order
        db.add(collaboration)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project reordered successfully"
            }, status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=500
        )