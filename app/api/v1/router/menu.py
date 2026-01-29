from fastapi import UploadFile
from app.services.menu import *
from app.core.session import get_db
from app.api.v1.schema.menu import *
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, Query

router = APIRouter()

@router.get("/all")
async def get_menus_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_menus(
        lang_code=lang_code,
        db=db
    )

@router.post("/item/create")
async def create_menu_item_endpoint(
    request: AddMenuItems,
    db: AsyncSession = Depends(get_db)
):
    return await add_menu_items(
        request=request,
        db=db
    )

@router.post("/create")
async def create_menu_endpoint(
    request: CreateMenu,
    db: AsyncSession = Depends(get_db)
):
    return await create_menu(
        request=request,
        db=db
    )