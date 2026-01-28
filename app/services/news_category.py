import os
import random
from datetime import datetime
from typing import List, Optional
from app.core.session import get_db
from sqlalchemy import select, func
from app.core.session import get_db
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

def news_category_id_generator():
    return random.randint(100000, 999999)

async def create_news_category(
    az_title: str = Form(...),
    en_title: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        category_az_query = await db.execute(
            select(NewsCategory)
            .where(
                NewsCategoryTranslation.lang_code == "az",
                NewsCategoryTranslation.title == az_title
            )
        )

        category_en_query = await db.execute(
            select(NewsCategory)
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
            created_at=datetime.utcnow()
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
        
        await db.refresh(new_category)
        await db.refresh(new_category_translation_az)
        await db.refresh(new_category_translation_en)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "News cateogry created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_news_categories(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        category_query = await db.execute(
            select(NewsCategory)
        )

        categories = category_query.scalars().all()

        if not categories:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        category_arr = []

        for category in categories:
            category_translation_query = await db.execute(
                select(NewsCategoryTranslation)
                .where(
                    NewsCategoryTranslation.lang_code == lang_code,
                    NewsCategoryTranslation.category_id == category.category_id
                )
            )

            category_translation = category_translation_query.scalar_one_or_none()

            category_obj = {
                "category_id": category.category_id,
                "title": category_translation.title
            }

            category_arr.append(category_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News categories fetched successfully.",
                "news_categories": category_arr
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )