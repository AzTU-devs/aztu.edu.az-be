import os
import random
from datetime import datetime
from typing import List, Optional
from app.core.session import get_db
from sqlalchemy import select, func
from app.core.session import get_db
from app.api.v1.schema.menu import *
from app.models.news.news import News
from app.models.menu.menu import Menu
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.menu_items.menu_items import MenuItems
from fastapi import Depends, UploadFile, File, Form, status
from app.models.menu.menu_translation import MenuTranslation
from app.models.menu_items.menu_items_translation import MenuItemsTranslation

def menu_id_generator():
    return random.randint(100000, 999999)

def menu_item_id_generator():
    return random.randint(100000, 999999)

async def create_menu(
    request: CreateMenu,
    db: AsyncSession = Depends(get_db)
):
    try:
        menu_id = menu_id_generator()

        try:
            result = await db.execute(select(Menu))
            existing_menus = result.scalars().all()
            for menu in existing_menus:
                menu.display_order = (menu.display_order or 0) + 1
                db.add(menu)

            display_order = 1
        except UndefinedTableError:
            display_order = 1

        menu_translation_query_az = await db.execute(
            select(MenuTranslation)
            .where(
                MenuTranslation.title == request.az_title,
                MenuTranslation.lang_code == "az"
            )
        )

        menu_translation_query_en = await db.execute(
            select(MenuTranslation)
            .where(
                MenuTranslation.title == request.en_title,
                MenuTranslation.lang_code == "en"
            )
        )

        if (menu_translation_query_az.scalar_one_or_none() or menu_translation_query_en.scalar_one_or_none()):
            return JSONResponse(
                content={
                    "status_code": 409,
                    "message": "Title already exists"
                }, status_code=status.HTTP_409_CONFLICT
            )
        
        new_menu = Menu(
            menu_id=menu_id,
            category_id=request.category_id,
            url=request.url if request.url else None,
            display_order=display_order,
            created_at=datetime.utcnow()
        )

        new_menu_translation_az = MenuTranslation(
            menu_id=menu_id,
            lang_code="az",
            title=request.az_title
        )

        new_menu_translation_en = MenuTranslation(
            menu_id=menu_id,
            lang_code="en",
            title=request.en_title
        )

        db.add(new_menu)
        db.add(new_menu_translation_az)
        db.add(new_menu_translation_en)

        await db.commit()

        await db.refresh(new_menu)
        await db.refresh(new_menu_translation_az)
        await db.refresh(new_menu_translation_en)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Menu created successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_menus(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        menu_query = await db.execute(
            select(Menu)
        )

        menus = menu_query.scalars().all()

        if not menus:
            return JSONResponse(
                content={
                    "status_code": 204
                }, status_code=status.HTTP_204_NO_CONTENT
            )
        
        menu_arr = []

        for menu in menus:
            menu_translation_query = await db.execute(
                select(MenuTranslation)
                .where(
                    MenuTranslation.menu_id == menu.menu_id,
                    MenuTranslation.lang_code == lang_code
                )
            )

            menu_translation = menu_translation_query.scalar_one_or_none()

            menu_items_arr = []

            menu_items_query = await db.execute(
                select(MenuItems)
                .where(
                    MenuItems.menu_id == menu.menu_id,
                )
            )

            menu_items = menu_items_query.scalars().all()

            for menu_item in menu_items:
                menu_tr_query = await db.execute(
                    select(MenuTranslation)
                    .where(
                        MenuItemsTranslation.item_id == menu_item.item_id,
                        MenuItemsTranslation.lang_code == lang_code
                    )
                )

                menu_item_tr = menu_tr_query.scalar_one_or_none()

                menu_item_obj = {
                    "item_id": menu_item.item_id,
                    "url": menu_item.url,
                    "display_order": menu_item.display_order,
                    "tite": menu_item_tr.title,
                    "created_at": menu_item.created_at.isoformat() if menu_item.created_at else None
                }

                menu_items_arr.append(menu_item_obj)

            menu_obj = {
                "menu_id": menu.menu_id,
                "category_id": menu.category_id,
                "url": menu.url if menu.url else None,
                "display_order": menu.display_order,
                "title": menu_translation.title,
                "created_at": menu.created_at.isoformat() if menu.created_at else None,
                "menu_items": menu_items_arr
            }

            menu_arr.append(menu_obj)
        
        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Menu fetched successfully.",
                "menus": menu_arr
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def add_menu_items(
    request: AddMenuItems,
    db: AsyncSession = Depends(get_db)
):
    try:
        menu_query = await db.execute(
            select(Menu)
            .where(Menu.menu_id == request.menu_id)
        )

        menu = menu_query.scalar_one_or_none()

        if not menu:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Menu not found"
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        for item in request.items:
            item_id = menu_item_id_generator()

            try:
                result = await db.execute(select(MenuItems))
                existing_menu_items = result.scalars().all()
                for item in existing_menu_items:
                    item.display_order = (item.display_order or 0) + 1
                    db.add(item)

                display_order = 1
            except UndefinedTableError:
                display_order = 1

            new_menu_item = MenuItems(
                menu_id=request.menu_id,
                item_id=item_id,
                url=item.url,
                display_order=display_order,
                created_at=datetime.utcnow()
            )

            new_menu_item_tr_az = MenuItemsTranslation(
                item_id=item_id,
                lang_code="az",
                title=item.az_title
            )

            new_menu_item_tr_en = MenuItemsTranslation(
                item_id=item_id,
                lang_code="en",
                title=item.en_title
            )

            db.add(new_menu_item)
            db.add(new_menu_item_tr_az)
            db.add(new_menu_item_tr_en)

            await db.commit()

            await db.refresh(new_menu_item)
            await db.refresh(new_menu_item_tr_az)
            await db.refresh(new_menu_item_tr_en)
        
        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Menu items added successfully."
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )