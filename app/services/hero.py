import os
import random
from datetime import datetime
from app.core.session import get_db
from sqlalchemy import select, func
from app.models.hero.hero import Hero
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, UploadFile, File, Form, status, Query
from app.core.logger import get_logger

logger = get_logger(__name__)


def hero_id_generator():
    return random.randint(100000, 999999)


async def create_hero(
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_id = hero_id_generator()
        upload_dir = "app/static/hero/"
        os.makedirs(upload_dir, exist_ok=True)

        filename = video.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{hero_id}.{ext}")
        file_content = await video.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        video_path = f"static/hero/{hero_id}.{ext}"

        new_hero = Hero(
            hero_id=hero_id,
            video=video_path,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db.add(new_hero)
        await db.commit()
        await db.refresh(new_hero)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Hero created successfully.",
                "hero_id": hero_id
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


async def get_hero(
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_query = await db.execute(
            select(Hero).where(Hero.is_active == True).limit(1)
        )
        hero = hero_query.scalar_one_or_none()

        if not hero:
            return JSONResponse(
                content={"status_code": 204},
                status_code=status.HTTP_204_NO_CONTENT
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Hero fetched successfully.",
                "hero": {
                    "hero_id": hero.hero_id,
                    "video": hero.video,
                    "is_active": hero.is_active
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


async def get_admin_hero(
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Hero))
        total = total_query.scalar() or 0

        hero_query = await db.execute(select(Hero))
        heroes = hero_query.scalars().all()

        if not heroes:
            return JSONResponse(
                content={"status_code": 204},
                status_code=status.HTTP_204_NO_CONTENT
            )

        heroes_arr = [
            {
                "hero_id": h.hero_id,
                "video": h.video,
                "is_active": h.is_active,
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "updated_at": h.updated_at.isoformat() if h.updated_at else None
            }
            for h in heroes
        ]

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Heroes fetched successfully.",
                "heroes": heroes_arr,
                "total": total
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


async def update_hero(
    hero_id: int,
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_query = await db.execute(
            select(Hero).where(Hero.hero_id == hero_id)
        )
        hero = hero_query.scalar_one_or_none()

        if not hero:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Hero not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        upload_dir = "app/static/hero/"
        os.makedirs(upload_dir, exist_ok=True)

        filename = video.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{hero_id}.{ext}")
        file_content = await video.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        video_path = f"static/hero/{hero_id}.{ext}"

        hero.video = video_path
        hero.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(hero)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Hero updated successfully."
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


async def activate_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_query = await db.execute(
            select(Hero).where(Hero.hero_id == hero_id)
        )
        hero = hero_query.scalar_one_or_none()

        if not hero:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Hero not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        hero.is_active = True
        hero.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(hero)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Hero activated successfully."
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


async def deactivate_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_query = await db.execute(
            select(Hero).where(Hero.hero_id == hero_id)
        )
        hero = hero_query.scalar_one_or_none()

        if not hero:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Hero not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        hero.is_active = False
        hero.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(hero)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Hero deactivated successfully."
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


async def delete_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero_query = await db.execute(
            select(Hero).where(Hero.hero_id == hero_id)
        )
        hero = hero_query.scalar_one_or_none()

        if not hero:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Hero not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        await db.delete(hero)
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Hero deleted successfully."
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
