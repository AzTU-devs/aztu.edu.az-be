import os
import random
from datetime import datetime
from typing import List, Optional
from app.core.session import get_db
from sqlalchemy import select, func
from app.core.session import get_db
from app.api.v1.schema.news import *
from app.models.news.news import News
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.news.news_translation import NewsTranslation
from app.models.news_gallery.news_gallery import NewsGallery
from app.models.news_category.news_category import NewsCategory
from fastapi import Depends, UploadFile, File, Form, status, Query
from app.models.news_category.news_category_translation import NewsCategoryTranslation

def news_id_generator():
    return random.randint(100000, 999999)

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
    try:
        news_id = news_id_generator()
        upload_dir = "app/static/news/"
        os.makedirs(upload_dir, exist_ok=True)
        filename = cover_image.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{news_id}.{ext}")
        file_content = await cover_image.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        image_path = f"static/news/{news_id}.{ext}"

        try:
            result = await db.execute(select(News))
            existing_announcements = result.scalars().all()
            for announcement in existing_announcements:
                announcement.display_order = (announcement.display_order or 0) + 1
                db.add(announcement)
            display_order = 1
        except UndefinedTableError:
            display_order = 1
        
        news_query_az = await db.execute(
            select(News)
            .where(
                NewsTranslation.title == az_title,
                NewsTranslation.lang_code == "az"
            )
        )

        news_query_en = await db.execute(
            select(News)
            .where(
                NewsTranslation.title == en_title,
                NewsTranslation.lang_code == "en"
            )
        )

        if (news_query_az.scalar_one_or_none() or news_query_en.scalar_one_or_none()):
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "News title already exists."
                }, status_code=status.HTTP_409_CONFLICT
            )
        
        category_query = await db.execute(
            select(NewsCategory)
            .where(NewsCategory.category_id == category_id)
        )

        news_category = category_query.scalar_one_or_none()

        if not news_category:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News category not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        new_news = News(
            news_id=news_id,
            category_id=category_id,
            display_order=display_order,
            is_active=True,
            created_at=datetime.utcnow()
        )

        new_news_translation_az = NewsTranslation(
            news_id=news_id,
            lang_code="az",
            title=az_title,
            html_content=az_html_content
        )

        new_news_translation_en = NewsTranslation(
            news_id=news_id,
            lang_code="en",
            title=en_title,
            html_content=en_html_content
        )

        new_news_cover_gallery = NewsGallery(
            news_id=news_id,
            image=image_path,
            is_cover=True
        )

        db.add(new_news)
        db.add(new_news_translation_az)
        db.add(new_news_translation_en)
        db.add(new_news_cover_gallery)
        await db.commit()
        await db.refresh(new_news)
        await db.refresh(new_news_translation_az)
        await db.refresh(new_news_translation_en)
        await db.refresh(new_news_cover_gallery)

        for index, gallery_image in enumerate(gallery_images or [], start=1):
            filename = gallery_image.filename
            ext = filename.split(".")[-1]

            gallery_filename = f"{news_id}-gallery-{index}.{ext}"
            file_path = os.path.join(upload_dir, gallery_filename)

            file_content = await gallery_image.read()
            with open(file_path, "wb") as f:
                f.write(file_content)

            image_path = f"static/news/{gallery_filename}"

            new_news_gallery = NewsGallery(
                news_id=news_id,
                image=image_path,
                is_cover=False
            )

            db.add(new_news_gallery)
            await db.commit()
            await db.refresh(new_news_gallery)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "News created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_public_news(
    category_id: int,
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(News))
        total = total_query.scalar() or 0

        news_query = await db.execute(
            select(News)
            .order_by(News.display_order.asc())
            .offset(start)
            .limit(end - start)
            .where(
                News.is_active == True,
                News.category_id == category_id
            )
        )

        fetched_news = news_query.scalars().all()

        if not fetched_news:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        news_arr = []

        for news in fetched_news:
            news_translation_query = await db.execute(
                select(NewsTranslation)
                .where(
                    NewsTranslation.news_id == news.news_id,
                    NewsTranslation.lang_code == lang_code
                )
            )

            news_translation = news_translation_query.scalar_one_or_none()

            cover_query = await db.execute(
                select(NewsGallery)
                .where(
                    NewsGallery.news_id == news.news_id,
                    NewsGallery.is_cover == True
                )
            )

            cover_image = cover_query.scalar_one_or_none()

            category_query = await db.execute(
                select(NewsCategoryTranslation)
                .where(
                    NewsCategoryTranslation.category_id == news.category_id,
                    NewsCategoryTranslation.lang_code == lang_code
                )
            )

            category = category_query.scalar_one_or_none()

            news_obj = {
                "news_id": news.news_id,
                "cateogry_id": category.title,
                "display_order": news.display_order,
                "is_active": news.is_active,
                "title": news_translation.title,
                "html_content": news_translation.html_content,
                "cover_image": cover_image.image,
                "created_at": news.created_at
            }

            news_arr.append(news_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News fetched successfully.",
                "news": news_arr,
                "total": total
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_admin_news(
    category_id: int,
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(News))
        total = total_query.scalar() or 0

        news_query = await db.execute(
            select(News)
            .order_by(News.display_order.asc())
            .offset(start)
            .limit(end - start)
            .where(
                News.category_id == category_id
            )
        )

        fetched_news = news_query.scalars().all()

        if not fetched_news:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        news_arr = []

        for news in fetched_news:
            news_translation_query = await db.execute(
                select(NewsTranslation)
                .where(
                    NewsTranslation.news_id == news.news_id,
                    NewsTranslation.lang_code == lang_code
                )
            )

            news_translation = news_translation_query.scalar_one_or_none()

            news_obj = {
                "news_id": news.news_id,
                "cateogry_id": news.category_id,
                "display_order": news.display_order,
                "is_active": news.is_active,
                "title": news_translation.title,
                "created_at": news.created_at.isoformat() if news.created_at else None
            }

            news_arr.append(news_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News fetched successfully.",
                "news": news_arr,
                "total": total
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_news_details(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news_query = await db.execute(
            select(News)
            .where(News.news_id == news_id)
        )

        news = news_query.scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        news_translation_query_az = await db.execute(
            select(NewsTranslation)
            .where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "az"
            )
        )

        news_translation_az = news_translation_query_az.scalar_one_or_none()

        news_translation_query_en = await db.execute(
            select(NewsTranslation)
            .where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "en"
            )
        )

        news_translation_en = news_translation_query_en.scalar_one_or_none()

        category_query = await db.execute(
            select(NewsCategoryTranslation)
            .where(
                NewsCategoryTranslation.category_id == news.category_id,
                NewsCategoryTranslation.lang_code == "az"
            )
        )

        news_category = category_query.scalar_one_or_none()

        cover_image_query = await db.execute(
            select(NewsGallery)
            .where(
                NewsGallery.news_id == news_id,
                NewsGallery.is_cover == True
            )
        )

        cover_image = cover_image_query.scalar_one_or_none()

        gallery_images_query = await db.execute(
            select(NewsGallery)
            .where(
                NewsGallery.news_id == news_id,
                NewsGallery.is_cover == False
            )
        )

        gallery_images = gallery_images_query.scalars().all()


        gallery_images_arr = []

        for gallery_image in gallery_images:
            gallery_image_obj = {
                "image_id": gallery_image.id,
                "image": gallery_image.image
            }

            gallery_images_arr.append(gallery_image_obj)
        
        news_obj = {
            "news_id": news.news_id,
            "az_title": news_translation_az.title,
            "az_html_content": news_translation_az.html_content,
            "en_title": news_translation_en.title,
            "en_html_content": news_translation_en.html_content,
            "category_id": news_category.title,
            "cover_image": cover_image.image,
            "gallery_images": gallery_images_arr
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News details fetced successfully.",
                "news": news_obj
            }
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def deactivate_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news_query = await db.execute(
            select(News)
            .where(News.news_id == news_id)
        )

        news = news_query.scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        news.is_active = False

        await db.commit()
        await db.refresh(news)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News deactivated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def activate_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news_query = await db.execute(
            select(News)
            .where(News.news_id == news_id)
        )

        news = news_query.scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        news.is_active = True

        await db.commit()
        await db.refresh(news)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News activated successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_news_gallery(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news_query = await db.execute(
            select(News)
            .where(News.news_id == news_id)
        )

        news = news_query.scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News not found."
                }, status_code=status.HTTP_404_NOT_FOUND    
            )
        
        gallery_query = await db.execute(
            select(NewsGallery)
            .where(NewsGallery.news_id == news_id)
        )

        gallery_images = gallery_query.scalars().all()

        if not gallery_images:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        gallery_images_arr = []

        for gallery_image in gallery_images:
            gallery_image_obj = {
                "id": gallery_image.id,
                "news_id": gallery_image.news_id,
                "image": gallery_image.image
            }

            gallery_images_arr.append(gallery_image_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News gallery fetched successfull.",
                "gallery_images": gallery_images_arr
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def reorder_news(
    request: ReOrderNews,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(News).where(News.news_id == request.news_id))

        news_to_move = result.scalar_one_or_none()

        if not news_to_move:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "error": "Project not found"
                }, status_code=404
            )

        old_order = news_to_move.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(
                content={
                    "status_code": 200,
                    "message": "No change"
                }, status_code=200)

        if new_order < old_order:
            result = await db.execute(
                select(News).where(
                    News.display_order >= new_order,
                    News.display_order < old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order += 1
                db.add(p)
        else:
            result = await db.execute(
                select(News).where(
                    News.display_order <= new_order,
                    News.display_order > old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order -= 1
                db.add(p)

        news_to_move.display_order = new_order
        db.add(news_to_move)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project reordered successfully"
            }, status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=500
        )

async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        news_query = await db.execute(
            select(News)
            .where(News.news_id == news_id)
        )

        news = news_query.scalar_one_or_none()

        if not news:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "News not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        news_translation_az_query = await db.execute(
            select(NewsTranslation)
            .where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "az"
            )
        )

        news_translation_en_query = await db.execute(
            select(NewsTranslation)
            .where(
                NewsTranslation.news_id == news_id,
                NewsTranslation.lang_code == "en"
            )
        )


        news_translation_az = news_translation_az_query.scalar_one_or_none()
        news_translation_en = news_translation_en_query.scalar_one_or_none()

        await db.delete(news)
        await db.delete(news_translation_az)
        await db.delete(news_translation_en)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "News deleted successfully."
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )