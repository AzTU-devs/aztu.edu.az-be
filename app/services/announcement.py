import os
import random
from datetime import datetime
from app.core.session import get_db
from sqlalchemy import select, func
from app.core.session import get_db
from app.api.v1.schema.project import *
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.announcement import *
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, Query, File
from asyncpg.exceptions import UndefinedTableError
from app.models.announcement.announcement import Announcement
from app.models.announcement.announcement_translation import AnnouncementTranslation

def announcement_id_generator():
    return random.randint(100000, 999999)

async def create_announcement(
    image: UploadFile = File(...),
    az_title: str = Form(...),
    az_html_content: str = Form(...),
    en_title: str = Form(...),
    en_html_content: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        announcement_id = announcement_id_generator()
        upload_dir = "app/static/announcements/"
        os.makedirs(upload_dir, exist_ok=True)
        filename = image.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{announcement_id}.{ext}")
        file_content = await image.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        image_path = f"static/announcements/{announcement_id}.{ext}"

        try:
            result = await db.execute(select(Announcement))
            existing_announcements = result.scalars().all()
            for announcement in existing_announcements:
                announcement.display_order = (announcement.display_order or 0) + 1
                db.add(announcement)
            display_order = 1
        except UndefinedTableError:
            display_order = 1
        
        new_announcement = Announcement(
            announcement_id=announcement_id,
            image=image_path,
            display_order=display_order,
            is_active=False,
            created_at=datetime.utcnow()
        )

        new_announcement_translation_az = AnnouncementTranslation(
            announcement_id=announcement_id,
            lang_code='az',
            title=az_title,
            html_content=az_html_content
        )

        new_announcement_translation_en = AnnouncementTranslation(
            announcement_id=announcement_id,
            lang_code='en',
            title=en_title,
            html_content=en_html_content
        )

        db.add(new_announcement)
        db.add(new_announcement_translation_az)
        db.add(new_announcement_translation_en)
        await db.commit()
        await db.refresh(new_announcement)
        await db.refresh(new_announcement_translation_az)
        await db.refresh(new_announcement_translation_en)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Announcement created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_announcements(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Announcement))
        total = total_query.scalar() or 0

        announcement_query = await db.execute(
            select(Announcement)
            .order_by(Announcement.display_order.asc())
            .offset(start)
            .limit(end - start)
        )

        announcements = announcement_query.scalars().all()

        if not announcements:
            return JSONResponse(
                content={
                    "status_code": 204,
                    "message": "No content."
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        announcement_arr = []

        for announcement in announcements:
            translation_query = await db.execute(
                select(AnnouncementTranslation)
                .where(
                    AnnouncementTranslation.announcement_id == announcement.announcement_id,
                    AnnouncementTranslation.lang_code == lang
                )
            )

            translation = translation_query.scalar_one_or_none()

            announcement_obj = {
                "id": announcement.announcement_id,
                "display_order": announcement.display_order,
                "title": translation.title,
                "html_content": translation.html_content,
                "is_active": announcement.is_active,
                "created_at": announcement.created_at.isoformat()
            }

            announcement_arr.append(announcement_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Announcements fetched successfully.",
                "announcements": announcement_arr
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_announcement(
    announcement_id: int,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        announcement_query = await db.execute(
            select(Announcement)
            .where(Announcement.announcement_id == announcement_id)
        )

        announcement = announcement_query.scalar_one_or_none()

        if not announcement:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Announcement not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        translation_query = await db.execute(
            select(AnnouncementTranslation)
            .where(
                AnnouncementTranslation.announcement_id == announcement_id,
                AnnouncementTranslation.lang_code == lang_code
            )
        )

        translation = translation_query.scalar_one_or_none()

        announcement_obj = {
            "announcement_id": announcement.announcement_id,
            "title": translation.title,
            "html_content": translation.html_content,
            "image": announcement.image,
            "display_order": announcement.display_order,
            "is_active": announcement.is_active,
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Announcement details fetched successfully.",
                "announcement": announcement_obj
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def deactivate_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        announcement_query = await db.execute(
            select(Announcement)
            .where(Announcement.announcement_id == announcement_id)
        )

        announcement = announcement_query.scalar_one_or_none()

        if not announcement:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Announcement not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        announcement.is_active = True

        await db.commit()

        await db.refresh(announcement)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Announcement deactivated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def activate_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        announcement_query = await db.execute(
            select(Announcement)
            .where(Announcement.announcement_id == announcement_id)
        )

        announcement = announcement_query.scalar_one_or_none()

        if not announcement:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Announcement not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        announcement.is_active = False

        await db.commit()

        await db.refresh(announcement)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Announcement deactivated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )