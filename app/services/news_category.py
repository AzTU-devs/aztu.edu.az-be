import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select, func
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)
from app.models.news.news import News
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.api.v1.schema.announcement import *
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from fastapi import Depends, UploadFile, File, Form, status
from app.models.news.news_translation import NewsTranslation
from app.models.news_gallery.news_gallery import NewsGallery
from app.models.news_category.news_category import NewsCategory
from app.models.news_category.news_category_translation import NewsCategoryTranslation

def news_category_id_generator() -> int:
    return secrets.randbelow(900000) + 100000

async def create_news_category(
    az_title: str = Form(...),
    en_title: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        category_az_query = await db.execute(
            select(NewsCategory)
            .join(NewsCategoryTranslation, NewsCategoryTranslation.category_id == NewsCategory.category_id)
            .where(
                NewsCategoryTranslation.lang_code == "az",
                NewsCategoryTranslation.title == az_title
            )
        )

        category_en_query = await db.execute(
            select(NewsCategory)
            .join(NewsCategoryTranslation, NewsCategoryTranslation.category_id == NewsCategory.category_id)
            .where(
                NewsCategoryTranslation.lang_code == "en",
                NewsCategoryTranslation.title == en_title
            )
        )

        if (category_az_query.scalar_one_or_none() or category_en_query.scalar_one_or_none()):
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Category already exists."
                }, status_code=status.HTTP_409_CONFLICT
            )

        category_id = news_category_id_generator()

        new_category = NewsCategory(
            category_id=category_id,
            created_at=datetime.now(timezone.utc)
        )

        new_category_translation_az = NewsCategoryTranslation(
            category_id=category_id,
            lang_code="az",
            title=az_title
        )

        new_category_translation_en = NewsCategoryTranslation(
            category_id=category_id,
            lang_code="en",
            title=en_title
        )

        db.add(new_category)
        db.add(new_category_translation_az)
        db.add(new_category_translation_en)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "News category created successfully."
            }, status_code=status.HTTP_201_CREATED
        )

    except Exception:
        logger.exception("Failed to create news category")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": "Internal server error"
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_news_categories(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        category_query = await db.execute(
            select(NewsCategory).order_by(NewsCategory.created_at.asc())
        )

        categories = category_query.scalars().all()

        if not categories:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )

        # Bulk fetch translations & counts (avoid N+1)
        ids = [c.category_id for c in categories]

        tr_rows = (await db.execute(
            select(NewsCategoryTranslation).where(
                NewsCategoryTranslation.category_id.in_(ids),
                NewsCategoryTranslation.lang_code == lang_code,
            )
        )).scalars().all()
        tr_by_id = {t.category_id: t for t in tr_rows}

        count_rows = (await db.execute(
            select(News.category_id, func.count(News.id))
            .where(News.category_id.in_(ids))
            .group_by(News.category_id)
        )).all()
        count_by_id = {cid: cnt for cid, cnt in count_rows}

        category_arr = []
        for category in categories:
            tr = tr_by_id.get(category.category_id)
            category_arr.append({
                "category_id": category.category_id,
                "title": tr.title if tr else None,
                "news_count": int(count_by_id.get(category.category_id, 0)),
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News categories fetched successfully.",
                "news_categories": category_arr
            }, status_code=status.HTTP_200_OK
        )

    except Exception:
        logger.exception("Failed to fetch news categories")
        return JSONResponse(
            content={
                "status_code": 500,
                "error": "Internal server error"
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_news_category_details(
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = (await db.execute(
            select(NewsCategory).where(NewsCategory.category_id == category_id)
        )).scalar_one_or_none()
        if not category:
            return JSONResponse(
                content={"status_code": 404, "message": "News category not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_az = (await db.execute(
            select(NewsCategoryTranslation).where(
                NewsCategoryTranslation.category_id == category_id,
                NewsCategoryTranslation.lang_code == "az",
            )
        )).scalar_one_or_none()
        tr_en = (await db.execute(
            select(NewsCategoryTranslation).where(
                NewsCategoryTranslation.category_id == category_id,
                NewsCategoryTranslation.lang_code == "en",
            )
        )).scalar_one_or_none()

        news_count = (await db.execute(
            select(func.count(News.id)).where(News.category_id == category_id)
        )).scalar() or 0

        return JSONResponse(
            content={
                "status_code": 200,
                "category": {
                    "category_id": category.category_id,
                    "az_title": tr_az.title if tr_az else None,
                    "en_title": tr_en.title if tr_en else None,
                    "news_count": int(news_count),
                },
            }
        )
    except Exception:
        logger.exception("Failed to fetch news category details")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_news_category(
    category_id: int,
    az_title: Optional[str] = None,
    en_title: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = (await db.execute(
            select(NewsCategory).where(NewsCategory.category_id == category_id)
        )).scalar_one_or_none()
        if not category:
            return JSONResponse(
                content={"status_code": 404, "message": "News category not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if az_title is not None:
            tr_az = (await db.execute(
                select(NewsCategoryTranslation).where(
                    NewsCategoryTranslation.category_id == category_id,
                    NewsCategoryTranslation.lang_code == "az",
                )
            )).scalar_one_or_none()
            if tr_az:
                tr_az.title = az_title
            else:
                db.add(NewsCategoryTranslation(
                    category_id=category_id, lang_code="az", title=az_title
                ))

        if en_title is not None:
            tr_en = (await db.execute(
                select(NewsCategoryTranslation).where(
                    NewsCategoryTranslation.category_id == category_id,
                    NewsCategoryTranslation.lang_code == "en",
                )
            )).scalar_one_or_none()
            if tr_en:
                tr_en.title = en_title
            else:
                db.add(NewsCategoryTranslation(
                    category_id=category_id, lang_code="en", title=en_title
                ))

        category.updated_at = datetime.now(timezone.utc)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "News category updated successfully."}
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to update news category")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_news_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = (await db.execute(
            select(NewsCategory).where(NewsCategory.category_id == category_id)
        )).scalar_one_or_none()
        if not category:
            return JSONResponse(
                content={"status_code": 404, "message": "News category not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Block delete if news exist for this category
        news_count = (await db.execute(
            select(func.count(News.id)).where(News.category_id == category_id)
        )).scalar() or 0
        if news_count > 0:
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Cannot delete category that has news.",
                    "news_count": int(news_count),
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        translations = (await db.execute(
            select(NewsCategoryTranslation).where(
                NewsCategoryTranslation.category_id == category_id
            )
        )).scalars().all()
        for tr in translations:
            await db.delete(tr)
        await db.delete(category)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "News category deleted successfully."}
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete news category")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
