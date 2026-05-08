import secrets
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, func
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)
from app.api.v1.schema.project import *
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.announcement import *
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES, ALLOWED_DOC_MIMES
from app.utils.html_sanitizer import sanitize_html
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, Query, File, Form, UploadFile
from asyncpg.exceptions import UndefinedTableError
from app.models.announcement.announcement import Announcement
from app.models.announcement.announcement_translation import AnnouncementTranslation
from app.services.search import on_announcement_change, on_announcement_delete


def announcement_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


async def create_announcement(
    image: Optional[UploadFile] = File(None),
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

        image_path: Optional[str] = None
        if image is not None and getattr(image, "filename", None):
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

        now = datetime.now(timezone.utc)
        db.add(Announcement(
            announcement_id=announcement_id,
            image=image_path,
            display_order=display_order,
            is_active=True,
            created_at=now,
            published_date=now.date()
        ))
        db.add(AnnouncementTranslation(announcement_id=announcement_id, lang_code="az", title=az_title, html_content=az_html_content))
        db.add(AnnouncementTranslation(announcement_id=announcement_id, lang_code="en", title=en_title, html_content=en_html_content))
        await db.commit()
        await on_announcement_change(db, announcement_id)

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


async def upload_announcement_attachment(
    file: UploadFile,
    db: AsyncSession,
):
    try:
        url = await save_upload(
            file,
            "announcements/files",
            ALLOWED_DOC_MIMES,
            allow_extension_fallback=True,
        )
        return JSONResponse(
            content={
                "status_code": 201,
                "message": "File uploaded successfully.",
                "url": url,
                "filename": getattr(file, "filename", None) or "",
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        logger.exception("Failed to upload announcement attachment")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_announcement(
    announcement_id: int,
    image: Optional[UploadFile] = None,
    az_title: Optional[str] = None,
    az_html_content: Optional[str] = None,
    en_title: Optional[str] = None,
    en_html_content: Optional[str] = None,
    db: AsyncSession = None,
):
    saved_files: list[str] = []
    try:
        a = (await db.execute(
            select(Announcement).where(Announcement.announcement_id == announcement_id)
        )).scalars().first()
        if not a:
            return JSONResponse(
                content={"status_code": 404, "message": "Announcement not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_image: Optional[str] = None
        if image is not None and getattr(image, "filename", None):
            new_path = await save_upload(image, "announcements", ALLOWED_IMAGE_MIMES)
            saved_files.append(new_path)
            old_image = a.image
            a.image = new_path

        translations = (await db.execute(
            select(AnnouncementTranslation).where(
                AnnouncementTranslation.announcement_id == announcement_id
            )
        )).scalars().all()
        tr_by_lang = {tr.lang_code: tr for tr in translations}

        def _apply(lang_code: str, title: Optional[str], html: Optional[str]):
            tr = tr_by_lang.get(lang_code)
            if tr is None:
                return
            if title is not None:
                tr.title = title
            if html is not None:
                tr.html_content = sanitize_html(html)

        _apply("az", az_title, az_html_content)
        _apply("en", en_title, en_html_content)

        await db.commit()
        await on_announcement_change(db, announcement_id)

        if old_image:
            safe_delete_file(old_image)

        return JSONResponse(content={
            "status_code": 200,
            "message": "Announcement updated successfully.",
        })

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to update announcement")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            select(Announcement).order_by(Announcement.display_order.asc(), Announcement.published_date.desc().nullslast()).offset(start).limit(end - start)
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
            )).scalars().first()
            announcement_arr.append({
                "announcement_id": a.announcement_id,
                "display_order": a.display_order,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "is_active": a.is_active,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "published_date": a.published_date.isoformat() if a.published_date else None,
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
            .order_by(Announcement.display_order.asc(), Announcement.published_date.desc().nullslast())
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
            )).scalars().first()
            announcement_arr.append({
                "id": a.announcement_id,
                "display_order": a.display_order,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "is_active": a.is_active,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "published_date": a.published_date.isoformat() if a.published_date else None,
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
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalars().first()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)

        tr = (await db.execute(
            select(AnnouncementTranslation).where(
                AnnouncementTranslation.announcement_id == announcement_id,
                AnnouncementTranslation.lang_code == lang_code
            )
        )).scalars().first()

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
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "published_date": a.published_date.isoformat() if a.published_date else None,
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
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalars().first()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)
        a.is_active = False
        await db.commit()
        await on_announcement_change(db, announcement_id)
        return JSONResponse(content={"status_code": 200, "message": "Announcement deactivated successfully."})
    except Exception:
        logger.exception("Failed to deactivate announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def activate_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(select(Announcement).where(Announcement.announcement_id == announcement_id))).scalars().first()
        if not a:
            return JSONResponse(content={"status_code": 404, "message": "Announcement not found."}, status_code=status.HTTP_404_NOT_FOUND)
        a.is_active = True
        await db.commit()
        await on_announcement_change(db, announcement_id)
        return JSONResponse(content={"status_code": 200, "message": "Announcement activated successfully."})
    except Exception:
        logger.exception("Failed to activate announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def reorder_announcement(
    request: ReOrderAnnouncement,
    db: AsyncSession = Depends(get_db)
):
    try:
        all_rows = (await db.execute(
            select(Announcement)
            .order_by(Announcement.display_order.asc(), Announcement.created_at.desc())
            .with_for_update()
        )).scalars().all()

        target = next((a for a in all_rows if a.announcement_id == request.announcement_id), None)
        if not target:
            return JSONResponse(content={"status_code": 404, "error": "Announcement not found"}, status_code=404)

        total = len(all_rows)
        if total == 0:
            return JSONResponse(content={"status_code": 200, "message": "No change"})

        new_order = max(1, min(int(request.new_order), total))

        ordered = [a for a in all_rows if a.announcement_id != request.announcement_id]
        ordered.insert(new_order - 1, target)

        for idx, a in enumerate(ordered, start=1):
            if a.display_order != idx:
                a.display_order = idx

        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Announcement reordered successfully"})

    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder announcement")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)


async def delete_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        a = (await db.execute(
            select(Announcement).where(Announcement.announcement_id == announcement_id)
        )).scalars().first()
        if not a:
            return JSONResponse(
                content={"status_code": 404, "message": "Announcement not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        image_path = a.image

        translations = (await db.execute(
            select(AnnouncementTranslation).where(
                AnnouncementTranslation.announcement_id == announcement_id
            )
        )).scalars().all()
        for tr in translations:
            await db.delete(tr)

        await db.delete(a)
        await db.commit()
        await on_announcement_delete(announcement_id)

        if image_path:
            safe_delete_file(image_path)

        return JSONResponse(content={"status_code": 200, "message": "Announcement deleted successfully."})

    except Exception:
        await db.rollback()
        logger.exception("Failed to delete announcement")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
