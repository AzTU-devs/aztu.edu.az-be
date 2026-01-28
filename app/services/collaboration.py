import os
import random
from datetime import datetime
from typing import List, Optional
from app.core.session import get_db
from sqlalchemy import select, func
from app.core.session import get_db
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.collaboration import *
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.collaboration.collaboration import Collaboration
from fastapi import Depends, UploadFile, File, Form, status, Query
from app.models.collaboration.collaboration_translation import CollaborationTranslation

def collaboration_id_generator():
    return random.randint(100000, 999999)

async def create_collaboration(
    az_title: str = Form(...),
    en_title: str = Form(...),
    image: UploadFile = File(...),
    url: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    try:
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
            result = await db.execute(select(Collaboration))
            existing_collaborations = result.scalars().all()
            for collab in existing_collaborations:
                collab.display_order = (collab.display_order or 0) + 1
                db.add(collab)
            display_order = 1
        except UndefinedTableError:
            display_order = 1

        collab_query_az = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.title == az_title,
                CollaborationTranslation.lang_code == "az"
            )
        )

        collab_query_en = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.title == en_title,
                CollaborationTranslation.lang_code == "en"
            )
        )

        if (collab_query_en.scalar_one_or_none() or collab_query_az.scalar_one_or_none()):
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Collaboration title already exists"
                }, status_code=status.HTTP_409_CONFLICT
            )
        
        new_collab = Collaboration(
            collaboration_id=collaboration_id,
            display_order=display_order,
            image=image_path,
            url=url if url else None,
            is_active=True,
            created_at=datetime.utcnow()
        )

        new_collab_tr_az = CollaborationTranslation(
            collaboration_id=collaboration_id,
            title=az_title,
            lang_code="az"
        )

        new_collab_tr_en = CollaborationTranslation(
            collaboration_id=collaboration_id,
            title=en_title,
            lang_code="en"
        )

        db.add(new_collab)
        db.add(new_collab_tr_az)
        db.add(new_collab_tr_en)

        await db.commit()

        await db.refresh(new_collab)
        await db.refresh(new_collab_tr_az)
        await db.refresh(new_collab_tr_en)

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

async def get_public_collaboration(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
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

        collaborations = collab_query.scalars().all()

        if not collaborations:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        collaboration_arr = []
        
        for collaboration in collaborations:
            collab_tr_query = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collaboration.collaboration_id,
                    CollaborationTranslation.lang_code == lang_code
                )
            )

            collaboration_tr = collab_tr_query.scalar_one_or_none()

            collaboration_obj = {
                "collaboration_id": collaboration.collaboration_id,
                "display_order": collaboration.display_order,
                "image": collaboration.image,
                "url": collaboration.url,
                "title": collaboration_tr.title,
            }

            collaboration_arr.append(collaboration_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaborations fetched successfully.",
                "collaborations": collaboration_arr,
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

async def get_admin_collaboration(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
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
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        collaboration_arr = []
        
        for collaboration in collaborations:
            collab_tr_query_az = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collaboration.collaboration_id,
                    CollaborationTranslation.lang_code == "az"
                )
            )

            collaboration_tr_az = collab_tr_query_az.scalar_one_or_none()

            collab_tr_query_en = await db.execute(
                select(CollaborationTranslation)
                .where(
                    CollaborationTranslation.collaboration_id == collaboration.collaboration_id,
                    CollaborationTranslation.lang_code == "en"
                )
            )

            collaboration_tr_en = collab_tr_query_en.scalar_one_or_none()

            collaboration_obj = {
                "collaboration_id": collaboration.collaboration_id,
                "display_order": collaboration.display_order,
                "is_active": collaboration.is_active,
                "image": collaboration.image,
                "url": collaboration.url,
                "az_title": collaboration_tr_az.title,
                "en_title": collaboration_tr_en.title
            }

            collaboration_arr.append(collaboration_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Collaborations fetched successfully.",
                "collaborations": collaboration_arr,
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

async def reorder_collaboration(
    request: ReOrderCollaboration,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == request.collaboration_id)
        )

        collab_to_move = result.scalar_one_or_none()
        
        if not collab_to_move:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "error": "Collaboration not found"
                }, status_code=404
            )

        old_order = collab_to_move.display_order
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

        collab_to_move.display_order = new_order
        db.add(collab_to_move)

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

async def delete_collaboration(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Collaboration)
            .where(Collaboration.collaboration_id == collaboration_id)
        )

        collaboration = result.scalar_one_or_none()
        
        if not collaboration:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "error": "Collaboration not found"
                }, status_code=404
            )
        
        collab_tr_az_query = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.collaboration_id == create_collaboration,
                CollaborationTranslation.lang_code == "az"
            )
        )

        collab_tr_en_query = await db.execute(
            select(CollaborationTranslation)
            .where(
                CollaborationTranslation.collaboration_id == create_collaboration,
                CollaborationTranslation.lang_code == "en"
            )
        )

        collab_tr_az = collab_tr_az_query.scalar_one_or_none()
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
            }, status_code=500
        )