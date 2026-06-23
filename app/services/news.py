import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select, func, update
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
from app.services.search import on_news_change, on_news_delete


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
    created_at: Optional[str] = Form(None),
    sdg_numbers: Optional[List[int]] = None,
    faculty_code: Optional[str] = None,
    cafedra_code: Optional[str] = None,
    show_in_all_news: bool = True,
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []  # Track all saved files for cleanup on failure
    try:
        news_id = news_id_generator()

        created_at_dt = datetime.now(timezone.utc)
        if created_at:
            try:
                parsed = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                created_at_dt = parsed
            except ValueError:
                return JSONResponse(
                    content={"status_code": 400, "message": "Invalid created_at format."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        # Sanitize HTML content before storing (prevents XSS)
        az_html_content = sanitize_html(az_html_content)
        en_html_content = sanitize_html(en_html_content)

        # Safe file upload — validates MIME from actual bytes, random filename
        image_path = await save_upload(cover_image, "news", ALLOWED_IMAGE_MIMES)
        saved_files.append(image_path)

        try:
            # Place by created_at desc: count rows newer than this one → that many come before it.
            newer_count = (await db.execute(
                select(func.count()).select_from(News).where(News.created_at > created_at_dt)
            )).scalar() or 0
            display_order = newer_count + 1
            # Shift down only rows that will sit at or after this slot.
            await db.execute(
                update(News)
                .where(func.coalesce(News.display_order, 0) >= display_order)
                .values(display_order=func.coalesce(News.display_order, 0) + 1)
            )
        except UndefinedTableError:
            display_order = 1

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

        # Validate SDG numbers (1..17)
        clean_sdgs = None
        if sdg_numbers:
            try:
                clean_sdgs = sorted({int(n) for n in sdg_numbers if 1 <= int(n) <= 17})
            except (TypeError, ValueError):
                clean_sdgs = None

        # Validate faculty/cafedra codes if provided
        if faculty_code:
            from app.models.faculties.faculties import Faculty
            f = (await db.execute(
                select(Faculty).where(Faculty.faculty_code == faculty_code)
            )).scalar_one_or_none()
            if not f:
                for fpath in saved_files:
                    safe_delete_file(fpath)
                return JSONResponse(
                    content={"status_code": 404, "message": "Faculty not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
        if cafedra_code:
            from app.models.cafedras.cafedras import Cafedra
            c = (await db.execute(
                select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
            )).scalar_one_or_none()
            if not c:
                for fpath in saved_files:
                    safe_delete_file(fpath)
                return JSONResponse(
                    content={"status_code": 404, "message": "Cafedra not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

        new_news = News(
            news_id=news_id,
            category_id=category_id,
            display_order=display_order,
            is_active=True,
            sdg_numbers=clean_sdgs,
            faculty_code=faculty_code or None,
            cafedra_code=cafedra_code or None,
            show_in_all_news=bool(show_in_all_news),
            created_at=created_at_dt
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
        await on_news_change(db, news_id)

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
    end: int = Query(10, gt=0, description="End index (absolute offset)"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        count_query = (
            select(func.count())
            .select_from(News)
            .where(News.is_active == True)  # noqa: E712
            .where(News.show_in_all_news == True)  # noqa: E712
        )
        if category_id is not None:
            count_query = count_query.where(News.category_id == category_id)
        total_query = await db.execute(count_query)
        total = total_query.scalar() or 0

        # start/end are absolute offsets; cap the page size (not the offset) so
        # deep pagination keeps working without rejecting large `end` values.
        page_size = min(max(end - start, 0), 100)

        query = (
            select(News)
            .where(News.is_active == True)  # noqa: E712
            .where(News.show_in_all_news == True)  # noqa: E712
            .order_by(News.display_order.asc(), News.created_at.desc())
            .offset(start)
            .limit(page_size)
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
                "sdg_numbers": news.sdg_numbers or [],
                "faculty_code": news.faculty_code,
                "cafedra_code": news.cafedra_code,
                "show_in_all_news": news.show_in_all_news,
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
    end: int = Query(10, gt=0, description="End index (absolute offset)"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        count_query = select(func.count()).select_from(News)
        if category_id is not None:
            count_query = count_query.where(News.category_id == category_id)
        total_query = await db.execute(count_query)
        total = total_query.scalar() or 0

        query = (
            select(News)
            .order_by(News.display_order.asc(), News.created_at.desc())
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

        covers = (await db.execute(
            select(NewsGallery)
            .where(NewsGallery.news_id.in_(news_ids))
            .order_by(NewsGallery.is_cover.desc(), NewsGallery.display_order.asc(), NewsGallery.id.asc())
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
                "sdg_numbers": news.sdg_numbers or [],
                "faculty_code": news.faculty_code,
                "cafedra_code": news.cafedra_code,
                "show_in_all_news": news.show_in_all_news,
                "title": tr.title if tr else None,
                "cover_image": cover.image if cover else None,
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

        cover = (await db.execute(
            select(NewsGallery)
            .where(NewsGallery.news_id == news_id)
            .order_by(NewsGallery.is_cover.desc(), NewsGallery.display_order.asc(), NewsGallery.id.asc())
            .limit(1)
        )).scalar_one_or_none()

        gallery = (await db.execute(
            select(NewsGallery)
            .where(
                NewsGallery.news_id == news_id,
                NewsGallery.is_cover == False  # noqa: E712
            )
            .order_by(NewsGallery.display_order.asc(), NewsGallery.id.asc())
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
                    "category_id": news.category_id,
                    "category_title": category.title if category else None,
                    "sdg_numbers": news.sdg_numbers or [],
                    "faculty_code": news.faculty_code,
                    "cafedra_code": news.cafedra_code,
                    "show_in_all_news": news.show_in_all_news,
                    "is_active": news.is_active,
                    "display_order": news.display_order,
                    "cover_image": cover.image if cover else None,
                    "cover_image_id": cover.id if cover else None,
                    "gallery_images": [
                        {"image_id": g.id, "image": g.image, "display_order": g.display_order}
                        for g in gallery
                    ],
                    "created_at": news.created_at.isoformat() if news.created_at else None,
                    "updated_at": news.updated_at.isoformat() if news.updated_at else None,
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
        await on_news_change(db, news_id)
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
        await on_news_change(db, news_id)
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
            select(NewsGallery)
            .where(NewsGallery.news_id == news_id)
            .order_by(NewsGallery.is_cover.desc(), NewsGallery.display_order.asc(), NewsGallery.id.asc())
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


def _resequence_display_order(rows: list, target, new_order: int) -> None:
    """Move `target` to position `new_order` (1-based) within `rows` and renumber 1..N.

    `rows` must already be ordered by current display_order. Mutates display_order in
    place; clamps out-of-range positions to the valid [1, total] window.
    """
    total = len(rows)
    if total == 0:
        return
    new_order = max(1, min(int(new_order), total))
    ordered = [r for r in rows if r is not target]
    ordered.insert(new_order - 1, target)
    for idx, r in enumerate(ordered, start=1):
        if r.display_order != idx:
            r.display_order = idx


async def reorder_news(
    request: ReOrderNews,
    db: AsyncSession = Depends(get_db)
):
    try:
        all_rows = (await db.execute(
            select(News).order_by(News.display_order.asc(), News.created_at.desc()).with_for_update()
        )).scalars().all()

        target = next((n for n in all_rows if n.news_id == request.news_id), None)
        if not target:
            return JSONResponse(content={"status_code": 404, "error": "News not found"}, status_code=404)

        _resequence_display_order(all_rows, target, request.new_order)

        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "News reordered successfully"})

    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def update_news(
    news_id: int,
    az_title: Optional[str] = None,
    en_title: Optional[str] = None,
    az_html_content: Optional[str] = None,
    en_html_content: Optional[str] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    cover_image: Optional[UploadFile] = None,
    new_gallery_images: Optional[List[UploadFile]] = None,
    removed_image_ids: Optional[List[int]] = None,
    gallery_order: Optional[List[dict]] = None,
    sdg_numbers: Optional[List[int]] = None,
    faculty_code: Optional[str] = None,
    cafedra_code: Optional[str] = None,
    clear_faculty: bool = False,
    clear_cafedra: bool = False,
    show_in_all_news: Optional[bool] = None,
    created_at: Optional[str] = None,
    display_order: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    saved_files: list[str] = []
    files_to_delete_after_commit: list[str] = []
    try:
        news = (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none()
        if not news:
            return JSONResponse(
                content={"status_code": 404, "message": "News not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if created_at is not None:
            try:
                parsed = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                news.created_at = parsed
            except ValueError:
                return JSONResponse(
                    content={"status_code": 400, "message": "Invalid created_at format."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        if category_id is not None:
            cat = (await db.execute(
                select(NewsCategory).where(NewsCategory.category_id == category_id)
            )).scalar_one_or_none()
            if not cat:
                return JSONResponse(
                    content={"status_code": 404, "message": "News category not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            news.category_id = category_id

        if is_active is not None:
            news.is_active = is_active

        if show_in_all_news is not None:
            news.show_in_all_news = bool(show_in_all_news)

        if sdg_numbers is not None:
            try:
                cleaned = sorted({int(n) for n in sdg_numbers if 1 <= int(n) <= 17})
                news.sdg_numbers = cleaned if cleaned else None
            except (TypeError, ValueError):
                pass

        if clear_faculty:
            news.faculty_code = None
        elif faculty_code is not None:
            from app.models.faculties.faculties import Faculty
            f = (await db.execute(
                select(Faculty).where(Faculty.faculty_code == faculty_code)
            )).scalar_one_or_none()
            if not f:
                return JSONResponse(
                    content={"status_code": 404, "message": "Faculty not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            news.faculty_code = faculty_code

        if clear_cafedra:
            news.cafedra_code = None
        elif cafedra_code is not None:
            from app.models.cafedras.cafedras import Cafedra
            c = (await db.execute(
                select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
            )).scalar_one_or_none()
            if not c:
                return JSONResponse(
                    content={"status_code": 404, "message": "Cafedra not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            news.cafedra_code = cafedra_code

        if az_title is not None or az_html_content is not None:
            tr_az = (await db.execute(
                select(NewsTranslation).where(
                    NewsTranslation.news_id == news_id,
                    NewsTranslation.lang_code == "az",
                )
            )).scalar_one_or_none()
            if tr_az:
                if az_title is not None:
                    tr_az.title = az_title
                if az_html_content is not None:
                    tr_az.html_content = sanitize_html(az_html_content)
            else:
                db.add(NewsTranslation(
                    news_id=news_id,
                    lang_code="az",
                    title=az_title or "",
                    html_content=sanitize_html(az_html_content or ""),
                ))

        if en_title is not None or en_html_content is not None:
            tr_en = (await db.execute(
                select(NewsTranslation).where(
                    NewsTranslation.news_id == news_id,
                    NewsTranslation.lang_code == "en",
                )
            )).scalar_one_or_none()
            if tr_en:
                if en_title is not None:
                    tr_en.title = en_title
                if en_html_content is not None:
                    tr_en.html_content = sanitize_html(en_html_content)
            else:
                db.add(NewsTranslation(
                    news_id=news_id,
                    lang_code="en",
                    title=en_title or "",
                    html_content=sanitize_html(en_html_content or ""),
                ))

        if cover_image is not None:
            old_cover = (await db.execute(
                select(NewsGallery).where(
                    NewsGallery.news_id == news_id,
                    NewsGallery.is_cover == True,  # noqa: E712
                )
            )).scalar_one_or_none()
            new_cover_path = await save_upload(cover_image, "news", ALLOWED_IMAGE_MIMES)
            saved_files.append(new_cover_path)
            if old_cover:
                files_to_delete_after_commit.append(old_cover.image)
                old_cover.image = new_cover_path
            else:
                db.add(NewsGallery(news_id=news_id, image=new_cover_path, is_cover=True, display_order=0))

        if removed_image_ids:
            to_remove = (await db.execute(
                select(NewsGallery).where(
                    NewsGallery.id.in_(removed_image_ids),
                    NewsGallery.news_id == news_id,
                    NewsGallery.is_cover == False,  # noqa: E712
                )
            )).scalars().all()
            for g in to_remove:
                files_to_delete_after_commit.append(g.image)
                await db.delete(g)

        if new_gallery_images:
            max_order_q = await db.execute(
                select(func.coalesce(func.max(NewsGallery.display_order), 0)).where(
                    NewsGallery.news_id == news_id,
                    NewsGallery.is_cover == False,  # noqa: E712
                )
            )
            next_order = (max_order_q.scalar() or 0) + 1
            for img in new_gallery_images:
                path = await save_upload(img, "news", ALLOWED_IMAGE_MIMES)
                saved_files.append(path)
                db.add(NewsGallery(
                    news_id=news_id,
                    image=path,
                    is_cover=False,
                    display_order=next_order,
                ))
                next_order += 1

        if gallery_order:
            order_map = {int(item["image_id"]): int(item["display_order"]) for item in gallery_order}
            rows = (await db.execute(
                select(NewsGallery).where(
                    NewsGallery.id.in_(list(order_map.keys())),
                    NewsGallery.news_id == news_id,
                )
            )).scalars().all()
            for r in rows:
                r.display_order = order_map[r.id]

        if display_order is not None:
            all_rows = (await db.execute(
                select(News).order_by(News.display_order.asc(), News.created_at.desc()).with_for_update()
            )).scalars().all()
            _resequence_display_order(all_rows, news, display_order)

        news.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await on_news_change(db, news_id)

        for path in files_to_delete_after_commit:
            safe_delete_file(path)

        return JSONResponse(
            content={"status_code": 200, "message": "News updated successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to update news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        await on_news_delete(news_id)

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


async def _get_news_by_owner(
    owner_filter,
    start: int,
    end: int,
    lang_code: str,
    db: AsyncSession,
):
    total = (await db.execute(
        select(func.count()).select_from(News)
        .where(News.is_active == True)  # noqa: E712
        .where(owner_filter)
    )).scalar() or 0

    # Cap page size (end-start), not the absolute offset, so deep pagination works.
    page_size = min(max(end - start, 0), 100)

    fetched_news = (await db.execute(
        select(News)
        .where(News.is_active == True)  # noqa: E712
        .where(owner_filter)
        .order_by(News.created_at.desc())
        .offset(start)
        .limit(page_size)
    )).scalars().all()

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
            "show_in_all_news": news.show_in_all_news,
            "sdg_numbers": news.sdg_numbers or [],
            "faculty_code": news.faculty_code,
            "cafedra_code": news.cafedra_code,
            "title": tr.title if tr else None,
            "html_content": tr.html_content if tr else None,
            "cover_image": cover.image if cover else None,
            "created_at": news.created_at.isoformat() if news.created_at else None,
        })

    return JSONResponse(
        content={"status_code": 200, "message": "News fetched successfully.", "news": news_arr, "total": total},
        status_code=status.HTTP_200_OK,
    )


async def get_faculty_news(
    faculty_code: str,
    start: int = 0,
    end: int = 10,
    lang_code: str = "az",
    db: AsyncSession = Depends(get_db),
):
    try:
        return await _get_news_by_owner(
            News.faculty_code == faculty_code, start, end, lang_code, db
        )
    except Exception:
        logger.exception("Failed to fetch faculty news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_cafedra_news(
    cafedra_code: str,
    start: int = 0,
    end: int = 10,
    lang_code: str = "az",
    db: AsyncSession = Depends(get_db),
):
    try:
        return await _get_news_by_owner(
            News.cafedra_code == cafedra_code, start, end, lang_code, db
        )
    except Exception:
        logger.exception("Failed to fetch cafedra news")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
