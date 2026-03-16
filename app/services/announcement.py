import secrets
from datetime import datetime, timezone
from sqlalchemy import select, func
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)
from app.api.v1.schema.project import *
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.announcement import *
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.utils.html_sanitizer import sanitize_html
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, Query, File
from asyncpg.exceptions import UndefinedTableError
from app.models.announcement.announcement import Announcement
from app.models.announcement.announcement_translation import AnnouncementTranslation


def announcement_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


async def create_announcement(
    image: UploadFile = File(...),
    az_title: str = Form(...),
    az_html_content: str = Form(...),
    en_title: str = Form(...),
    en_html_content: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []
    try:
        announcement_id = announcement_id_generator()

        az_html_content = sanitize_html(az_html_content)
        en_html_content = sanitize_html(en_html_content)

        image_path = await save_upload(image, "announcements", ALLOWED_IMAGE_MIMES)
        saved_files.append(image_path)

        try:
            result = await db.execute(select(Announcement))
            for a in result.scalars().all():
                a.display_order = (a.display_order or 0) + 1
                db.add(a)
            display_order = 1
        except UndefinedTableError:
            display_order = 1

        db.add(Announcement(
            announcement_id=announcement_id,
            image=image_path,
            display_order=display_order,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        ))
        db.add(AnnouncementTranslation(announcement_id=announcement_id, lang_code="az", title=az_title, html_content=az_html_content))
        db.add(AnnouncementTranslation(announcement_id=announcement_id, lang_code="en", title=en_title, html_content=en_html_content))
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Announcement created successfully."},
            status_code=status.HTTP_201_CREATED
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create announcement")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_announcements_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, le=100, description="End index (max 100)"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(Announcement))).scalar() or 0

        announcements = (await db.execute(
            select(Announcement).order_by(Announcement.display_order.asc()).offset(start).limit(end - start)
        )).scalars().all()

        if not announcements:
            return JSONResponse(content={"status_code": 204, "message": "No content."}, status_code=status.HTTP_204_NO_CONTENT)

        announcement_arr = []
        for a in announcements:
            tr = (await db.execute(
                select(AnnouncementTranslation).where(
                    AnnouncementTranslation.announcement_id == a.announcement_id,
                    AnnouncementTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            announcement_arr.append({
                "announcement_id": a.announcement_id,
                "display_order": a.display_order,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "is_active": a.is_active,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "Announcements fetched successfully.", "announcements": announcement_arr, "total": total}
        )

    except Exception:
        logger.exception("Failed to fetch admin announcements")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_announcements_user(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, le=100, description="End index (max 100)"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(Announcement))).scalar() or 0

        announcements = (await db.execute(
            select(Announcement)
            .where(Announcement.is_active == True)  # noqa: E712
            .order_by(Announcement.display_order.asc())
            .offset(start).limit(end - start)
        )).scalars().all()

        if not announcements:
            return JSONResponse(content={"status_code": 204, "message": "No content."}, status_code=status.HTTP_204_NO_CONTENT)

        announcement_arr = []
        for a in announcements:
            tr = (await db.execute(
                select(AnnouncementTranslation).where(
                    AnnouncementTranslation.announcement_id == a.announcement_id,
                    AnnouncementTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            announcement_arr.append({
                "id": a.announcement_id,
                "display_order": a.display_order,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "is_active": a.is_active,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "Announcements fetched successfully.", "announcements": announcement_arr}
        )

    except Exception:
        logger.exception("Failed to fetch user announcements")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_announcement(
    announcement_id: int,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalar_one_or_none()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)

        tr = (await db.execute(
            select(AnnouncementTranslation).where(
                AnnouncementTranslation.announcement_id == announcement_id,
                AnnouncementTranslation.lang_code == lang_code
            )
        )).scalar_one_or_none()

        return JSONResponse(content={
            "status_code": 200,
            "message": "Announcement details fetched successfully.",
            "announcement": {
                "announcement_id": a.announcement_id,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "image": a.image,
                "display_order": a.display_order,
                "is_active": a.is_active,
            }
        })

    except Exception:
        logger.exception("Failed to fetch announcement")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def deactivate_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalar_one_or_none()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)
        a.is_active = False
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Announcement deactivated successfully."})
    except Exception:
        logger.exception("Failed to deactivate announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def activate_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalar_one_or_none()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)
        a.is_active = True
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Announcement activated successfully."})
    except Exception:
        logger.exception("Failed to activate announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def reorder_announcement(
    request: ReOrderAnnouncement,
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == request.announcement_id))).scalar_one_or_none()
        if not a:
            return JSONResponse(content={"status_code": 404, "error": "Announcement not found"}, status_code=404)

        old_order = a.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(content={"status_code": 200, "message": "No change"})

        if new_order < old_order:
            rows = (await db.execute(
                select(Announcement).where(Announcement.display_order >= new_order, Announcement.display_order < old_order)
            )).scalars().all()
            for r in rows:
                r.display_order += 1
                db.add(r)
        else:
            rows = (await db.execute(
                select(Announcement).where(Announcement.display_order <= new_order, Announcement.display_order > old_order)
            )).scalars().all()
            for r in rows:
                r.display_order -= 1
                db.add(r)

        a.display_order = new_order
        db.add(a)
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Announcement reordered successfully"})

    except Exception:
        logger.exception("Failed to reorder announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)
