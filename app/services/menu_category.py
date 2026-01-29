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
from app.models.menu_category.menu_category import MenuCategory
from app.models.news_category.news_category_translation import NewsCategoryTranslation

def menu_category_id_generator():
    return random.randint(100000, 999999)

async def create_menu_category(
    title: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        category_id = menu_category_id_generator()

        title_query = await db.execute(
            select(MenuCategory)
            .where(MenuCategory.title == title)
        )

        exist_category = title_query.scalar_one_or_none()

        if exist_category:
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Menu category already exists."
                }, status_code=status.HTTP_409_CONFLICT
            )
        
        new_category = MenuCategory(
            category_id=category_id,
            title=title,
            created_at=datetime.utcnow()
        )

        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Menu category created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_menu_categories(
    db: AsyncSession = Depends(get_db)
):
    try:
        category_query = await db.execute(
            select(MenuCategory)
        )

        categories = category_query.scalars().all()

        if not categories:
            return JSONResponse(
                content={
                    "status_code": 204,
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        category_arr = []

        for category in categories:
            category_obj = {
                "title": category.title
            }

            category_arr.append(category_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Categories fetched successfully.",
                "categories": category_arr
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )