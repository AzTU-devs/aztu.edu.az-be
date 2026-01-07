from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language

from app.services.slider import (
    get_sliders,
    get_slider_by_id,
    create_slider,
    reorder_slider,
    delete_slider,
)

from app.api.v1.schema.slider import SliderCreate, ReOrderSlider

router = APIRouter()


@router.get("/all")
async def get_sliders_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_sliders(start=start, end=end, lang=lang, db=db)


@router.get("/{slider_id}")
async def get_slider_by_id_endpoint(
    slider_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_slider_by_id(slider_id=slider_id, lang=lang, db=db)


@router.post("/create")
async def create_slider_endpoint(
    image: UploadFile = File(...),
    az_desc: str = Form(...),
    en_desc: str = Form(...),
    url: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    request = SliderCreate.as_form(
        image=image,
        az_desc=az_desc,
        en_desc=en_desc,
        url=url,
    )
    return await create_slider(request=request, db=db)




@router.post("/reorder")
async def reorder_slider_endpoint(
    request: ReOrderSlider,
    db: AsyncSession = Depends(get_db),
):
    return await reorder_slider(request=request, db=db)


@router.delete("/{slider_id}/delete")
async def delete_slider_endpoint(
    slider_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_slider(slider_id=slider_id, db=db)
