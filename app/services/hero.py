import secrets
from datetime import datetime, timezone
from app.core.session import get_db
from sqlalchemy import select, func
from app.models.hero.hero import Hero
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, UploadFile, File, status
from app.core.logger import get_logger
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_VIDEO_MIMES

logger = get_logger(__name__)


def hero_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


async def create_hero(
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []
    try:
        hero_id = hero_id_generator()
        # Hero section accepts video files only
        video_path = await save_upload(video, "hero", ALLOWED_VIDEO_MIMES, max_size=100 * 1024 * 1024)
        saved_files.append(video_path)

        db.add(Hero(
            hero_id=hero_id,
            video=video_path,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        ))
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Hero created successfully.", "hero_id": hero_id},
            status_code=status.HTTP_201_CREATED
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_hero(
    db: AsyncSession = Depends(get_db)
):
    try:
        hero = (await db.execute(
            select(Hero).where(Hero.is_active == True).limit(1)  # noqa: E712
        )).scalar_one_or_none()

        if not hero:
            return JSONResponse(content={"status_code": 204}, status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(content={
            "status_code": 200,
            "message": "Hero fetched successfully.",
            "hero": {"hero_id": hero.hero_id, "video": hero.video, "is_active": hero.is_active}
        })

    except Exception:
        logger.exception("Failed to fetch hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_admin_hero(
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(Hero))).scalar() or 0
        heroes = (await db.execute(select(Hero))).scalars().all()

        if not heroes:
            return JSONResponse(content={"status_code": 204}, status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(content={
            "status_code": 200,
            "message": "Heroes fetched successfully.",
            "total": total,
            "heroes": [
                {
                    "hero_id": h.hero_id,
                    "video": h.video,
                    "is_active": h.is_active,
                    "created_at": h.created_at.isoformat() if h.created_at else None,
                    "updated_at": h.updated_at.isoformat() if h.updated_at else None,
                }
                for h in heroes
            ]
        })

    except Exception:
        logger.exception("Failed to fetch admin heroes")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_hero(
    hero_id: int,
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []
    try:
        hero = (await db.execute(select(Hero).where(Hero.hero_id == hero_id))).scalar_one_or_none()
        if not hero:
            return JSONResponse(content={"status_code": 404, "message": "Hero not found."}, status_code=status.HTTP_404_NOT_FOUND)

        old_video = hero.video
        new_video_path = await save_upload(video, "hero", ALLOWED_VIDEO_MIMES, max_size=100 * 1024 * 1024)
        saved_files.append(new_video_path)

        hero.video = new_video_path
        hero.updated_at = datetime.now(timezone.utc)
        await db.commit()

        safe_delete_file(old_video)

        return JSONResponse(content={"status_code": 200, "message": "Hero updated successfully."})

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to update hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def activate_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero = (await db.execute(select(Hero).where(Hero.hero_id == hero_id))).scalar_one_or_none()
        if not hero:
            return JSONResponse(content={"status_code": 404, "message": "Hero not found."}, status_code=status.HTTP_404_NOT_FOUND)
        hero.is_active = True
        hero.updated_at = datetime.now(timezone.utc)
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Hero activated successfully."})
    except Exception:
        logger.exception("Failed to activate hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def deactivate_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero = (await db.execute(select(Hero).where(Hero.hero_id == hero_id))).scalar_one_or_none()
        if not hero:
            return JSONResponse(content={"status_code": 404, "message": "Hero not found."}, status_code=status.HTTP_404_NOT_FOUND)
        hero.is_active = False
        hero.updated_at = datetime.now(timezone.utc)
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Hero deactivated successfully."})
    except Exception:
        logger.exception("Failed to deactivate hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def delete_hero(
    hero_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        hero = (await db.execute(select(Hero).where(Hero.hero_id == hero_id))).scalar_one_or_none()
        if not hero:
            return JSONResponse(content={"status_code": 404, "message": "Hero not found."}, status_code=status.HTTP_404_NOT_FOUND)

        video_path = hero.video
        await db.delete(hero)
        await db.commit()

        safe_delete_file(video_path)

        return JSONResponse(content={"status_code": 200, "message": "Hero deleted successfully."})

    except Exception:
        logger.exception("Failed to delete hero")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
