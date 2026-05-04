import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)
from app.api.v1.schema.news import *
from app.models.news.news import News
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.utils.html_sanitizer import sanitize_html
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.news.news_translation import NewsTranslation
from app.models.news_gallery.news_gallery import NewsGallery
from app.models.news_category.news_category import NewsCategory
from fastapi import Depends, UploadFile, File, Form, status, Query
from app.models.news_category.news_category_translation import NewsCategoryTranslation


def news_id_generator() -> int:
    # Cryptographically random ID — replaces insecure random.randint
    return secrets.randbelow(900000) + 100000


async def create_news(
    az_title: str = Form(...),
    en_title: str = Form(...),
    az_html_content: str = Form(...),
    en_html_content: str = Form(...),
    cover_image: UploadFile = File(...),
    gallery_images: Optional[List[UploadFile]] = File(None),
    category_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []  # Track all saved files for cleanup on failure
    try:
        news_id = news_id_generator()

        # Sanitize HTML content before storing (prevents XSS)
        az_html_content = sanitize_html(az_html_content)
        en_html_content = sanitize_html(en_html_content)

        # Safe file upload — validates MIME from actual bytes, random filename
        image_path = await save_upload(cover_image, "news", ALLOWED_IMAGE_MIMES)
        saved_files.append(image_path)

        try:
            # Single statement instead of fetching every row + per-row update.
            await db.execute(
                update(News).values(display_order=func.coalesce(News.display_order, 0) + 1)
            )
            display_order = 1
        except UndefinedTableError:
            display_order = 1

        news_query_az = await db.execute(
            select(News)
            .join(NewsTranslation, NewsTranslation.news_id == News.news_id)
            .where(
                NewsTranslation.title == az_title,
                NewsTranslation.lang_code == "az"
            )
        )
        news_query_en = await db.execute(
            select(News)
            .join(NewsTranslation, NewsTranslation.news_id == News.news_id)
            .where(
                NewsTranslation.title == en_title,
                NewsTranslation.lang_code == "en"
            )
        )

        if news_query_az.scalar_one_or_none() or news_query_en.scalar_one_or_none():
            for f in saved_files:
                safe_delete_file(f)
            return JSONResponse(
                content={"status_code": 409, "message": "News title already exists."},
                status_code=status.HTTP_409_CONFLICT
            )

        category_query = await db.execute(
            select(NewsCategory).where(NewsCategory.category_id == category_id)
        )
        if not category_query.scalar_one_or_none():
            for f in saved_files:
                safe_delete_file(f)
            return JSONResponse(
                content={"status_code": 404, "message": "News category not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        new_news = News(
            news_id=news_id,
            category_id=category_id,
            display_order=display_order,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_news)
        db.add(NewsTranslation(news_id=news_id, lang_code="az", title=az_title, html_content=az_html_content))
        db.add(NewsTranslation(news_id=news_id, lang_code="en", title=en_title, html_content=en_html_content))
        db.add(NewsGallery(news_id=news_id, image=image_path, is_cover=True))

        # Gallery images — all added in the same transaction before committing once
        for gallery_image in (gallery_images or []):
            gallery_path = await save_upload(gallery_image, "news", ALLOWED_IMAGE_MIMES)
            saved_files.append(gallery_path)
            db.add(NewsGallery(news_id=news_id, image=gallery_path, is_cover=False))

        # Single commit for the entire operation — atomic
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "News created successfully."},
            status_code=status.HTTP_201_CREATED
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_public_news(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, le=100, description="End index (max 100)"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(News))
        total = total_query.scalar() or 0

        query = (
            select(News)
            .where(News.is_active == True)  # noqa: E712
            .order_by(News.created_at.desc())
            .offset(start)
            .limit(end - start)
        )
        if category_id is not None:
            query = query.where(News.category_id == category_id)

        fetched_news = (await db.execute(query)).scalars().all()

        if not fetched_news:
            return JSONResponse(content={"status_code": 204}, status_code=status.HTTP_204_NO_CONTENT)

        news_ids = [n.news_id for n in fetched_news]

        translations = (await db.execute(
            select(NewsTranslation).where(
                NewsTranslation.news_id.in_(news_ids),
                NewsTranslation.lang_code == lang_code,
            )
        )).scalars().all()
        tr_by_id = {t.news_id: t for t in translations}

        # Earliest gallery row per news_id is the cover.
        covers = (await db.execute(
            select(NewsGallery).where(NewsGallery.news_id.in_(news_ids)).order_by(NewsGallery.id)
        )).scalars().all()
        cover_by_id: dict[int, NewsGallery] = {}
        for g in covers:
            cover_by_id.setdefault(g.news_id, g)

        news_arr = []
        for news in fetched_news:
            tr = tr_by_id.get(news.news_id)
            cover = cover_by_id.get(news.news_id)
            news_arr.append({
                "news_id": news.news_id,
                "category_id": news.category_id,
                "display_order": news.display_order,
                "is_active": news.is_active,
                "title": tr.title if tr else None,
                "html_content": tr.html_content if tr else None,
                "cover_image": cover.image if cover else None,
                "created_at": news.created_at.isoformat() if news.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "News fetched successfully.", "news": news_arr, "total": total},
            status_code=status.HTTP_200_OK
        )

    except Exception:
        logger.exception("Failed to fetch public news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_admin_news(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, le=100, description="End index (max 100)"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(News))
        total = total_query.scalar() or 0

        query = (
            select(News)
            .order_by(News.display_order.asc())
            .offset(start)
            .limit(end - start)
        )
        if category_id is not None:
            query = query.where(News.category_id == category_id)

        fetched_news = (await db.execute(query)).scalars().all()

        if not fetched_news:
            return JSONResponse(content={"status_code": 204}, status_code=status.HTTP_204_NO_CONTENT)

        news_ids = [n.news_id for n in fetched_news]
        translations = (await db.execute(
            select(NewsTranslation).where(
                NewsTranslation.news_id.in_(news_ids),
                NewsTranslation.lang_code == lang_code,
            )
        )).scalars().all()
        tr_by_id = {t.news_id: t for t in translations}

        news_arr = []
        for news in fetched_news:
            tr = tr_by_id.get(news.news_id)
            news_arr.append({
                "news_id": news.news_id,
                "category_id": news.category_id,
                "display_order": news.display_order,
                "is_active": news.is_active,
                "title": tr.title if tr else None,
                "created_at": news.created_at.isoformat() if news.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "News fetched successfully.", "news": news_arr, "total": total},
            status_code=status.HTTP_200_OK
        )

    except Exception:
        logger.exception("Failed to fetch admin news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_news_details(
    news_id: int,
    lang_code: str = "az",
    db: AsyncSession = Depends(get_db)
):
    try:
        news = (await db.execute(
            select(News).where(News.news_id == news_id)
        )).scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        tr_az = (await db.execute(
            select(NewsTranslation).where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "az"
            )
        )).scalar_one_or_none()

        tr_en = (await db.execute(
            select(NewsTranslation).where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "en"
            )
        )).scalar_one_or_none()

        tr = tr_en if lang_code == "en" else tr_az

        category = (await db.execute(
            select(NewsCategoryTranslation).where(
                NewsCategoryTranslation.category_id == news.category_id,
                NewsCategoryTranslation.lang_code == lang_code
            )
        )).scalar_one_or_none()

        # ✅ FIXED: deterministic cover selection
        cover = (await db.execute(
            select(NewsGallery)
            .where(NewsGallery.news_id == news_id)
            .order_by(NewsGallery.is_cover.desc(), NewsGallery.id.asc())
            .limit(1)
        )).scalar_one_or_none()

        # ✅ FIXED: deterministic gallery order
        gallery = (await db.execute(
            select(NewsGallery)
            .where(
                NewsGallery.news_id == news_id,
                NewsGallery.is_cover == False  # noqa: E712
            )
            .order_by(NewsGallery.id.asc())
        )).scalars().all()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News details fetched successfully.",
                "news": {
                    "news_id": news.news_id,
                    "title": tr.title if tr else None,
                    "html_content": tr.html_content if tr else None,
                    "az_title": tr_az.title if tr_az else None,
                    "az_html_content": tr_az.html_content if tr_az else None,
                    "en_title": tr_en.title if tr_en else None,
                    "en_html_content": tr_en.html_content if tr_en else None,
                    "category_id": category.title if category else None,
                    "cover_image": cover.image if cover else None,
                    "gallery_images": [
                        {"image_id": g.id, "image": g.image}
                        for g in gallery
                    ],
                }
            }
        )

    except Exception:
        logger.exception("Failed to fetch news details")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def deactivate_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news = (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none()
        if not news:
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )
        news.is_active = False
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "News deactivated successfully."})

    except Exception:
        logger.exception("Failed to deactivate news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def activate_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news = (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none()
        if not news:
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )
        news.is_active = True
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "News activated successfully."})

    except Exception:
        logger.exception("Failed to activate news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_news_gallery(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        if not (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        gallery = (await db.execute(
            select(NewsGallery).where(NewsGallery.news_id == news_id)
        )).scalars().all()

        if not gallery:
            return JSONResponse(content={"status_code": 204}, status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News gallery fetched successfully.",
                "gallery_images": [{"id": g.id, "news_id": g.news_id, "image": g.image} for g in gallery],
            }
        )

    except Exception:
        logger.exception("Failed to fetch news gallery")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def reorder_news(
    request: ReOrderNews,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Lock the target row first so concurrent reorder requests serialize.
        news_to_move = (await db.execute(
            select(News).where(News.news_id == request.news_id).with_for_update()
        )).scalar_one_or_none()
        if not news_to_move:
            return JSONResponse(content={"status_code": 404, "error": "News not found"}, status_code=404)

        old_order = news_to_move.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(content={"status_code": 200, "message": "No change"}, status_code=200)

        if new_order < old_order:
            await db.execute(
                update(News)
                .where(News.display_order >= new_order, News.display_order < old_order)
                .values(display_order=News.display_order + 1)
            )
        else:
            await db.execute(
                update(News)
                .where(News.display_order <= new_order, News.display_order > old_order)
                .values(display_order=News.display_order - 1)
            )

        news_to_move.display_order = new_order
        db.add(news_to_move)
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "News reordered successfully"})

    except Exception:
        logger.exception("Failed to reorder news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news = (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none()
        if not news:
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        gallery = (await db.execute(
            select(NewsGallery).where(NewsGallery.news_id == news_id)
        )).scalars().all()

        # Collect file paths before deleting records
        file_paths = [g.image for g in gallery]

        for g in gallery:
            await db.delete(g)

        translations = (await db.execute(
            select(NewsTranslation).where(NewsTranslation.news_id == news_id)
        )).scalars().all()
        for tr in translations:
            await db.delete(tr)

        await db.delete(news)
        await db.commit()

        # Delete files after successful DB commit — safe_delete_file prevents path traversal
        for path in file_paths:
            safe_delete_file(path)

        return JSONResponse(content={"status_code": 200, "message": "News deleted successfully."})

    except Exception:
        logger.exception("Failed to delete news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
