from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.api.v1.schema.cafedra import CreateCafedra, UpdateCafedra
from app.services.cafedra import (
    create_cafedra,
    delete_cafedra,
    get_cafedra,
    get_cafedras,
    update_cafedra,
)

router = APIRouter()


@router.get("/admin/all")
async def get_cafedras_endpoint_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/public/all")
async def get_cafedras_endpoint_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/{cafedra_code}")
async def get_cafedra_details_endpoint(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra(
        cafedra_code=cafedra_code,
        lang_code=lang_code,
        db=db,
    )


@router.post("/create")
async def create_cafedra_endpoint(
    request: CreateCafedra = Depends(CreateCafedra.as_form),
    db: AsyncSession = Depends(get_db),
):
    return await create_cafedra(
        request=request,
        db=db,
    )


@router.put("/{cafedra_code}")
async def update_cafedra_endpoint(
    cafedra_code: str,
    request: UpdateCafedra = Depends(UpdateCafedra.as_form),
    db: AsyncSession = Depends(get_db),
):
    return await update_cafedra(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.delete("/{cafedra_code}")
async def delete_cafedra_endpoint(
    cafedra_code: str,
    db: AsyncSession = Depends(get_db),
):
    return await delete_cafedra(
        cafedra_code=cafedra_code,
        db=db,
    )
