from app.services.collaboration import *
from app.core.session import get_db
from app.api.v1.schema.collaboration import *
from app.utils.language import get_language
from fastapi import APIRouter, Depends, File, Form, Query
from fastapi import UploadFile
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/all")
async def get_collaborations_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_collaborations(start=start, end=end, lang=lang, db=db)


@router.get("/{collaboration_id}")
async def get_collaboration_by_id_endpoint(
    collaboration_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_collaboration_by_id(collaboration_id=collaboration_id, lang=lang, db=db)


@router.post("/create", response_model=None)
async def create_collaboration_endpoint(
    logo: UploadFile = File(...),
    website_url: Optional[str] = Form(None),
    az_name: str = Form(...),
    en_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    request = CollaborationCreate.as_form(
        logo=logo,
        website_url=website_url,
        az_name=az_name,
        en_name=en_name
    )
    return await create_collaboration(request=request, db=db)


@router.put("/{collaboration_id}/update", response_model=None)
async def update_collaboration_endpoint(
    collaboration_id: int,
    logo: Optional[UploadFile] = File(None),
    website_url: Optional[str] = Form(None),
    az_name: str = Form(...),
    en_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    request = CollaborationUpdate.as_form(
        logo=logo,
        website_url=website_url,
        az_name=az_name,
        en_name=en_name
    )
    return await update_collaboration(collaboration_id=collaboration_id, request=request, db=db)


@router.post("/reorder")
async def reorder_collaboration_endpoint(
    request: ReOrderCollaboration,
    db: AsyncSession = Depends(get_db),
):
    return await reorder_collaboration(request=request, db=db)


@router.delete("/{collaboration_id}/delete")
async def delete_collaboration_endpoint(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_collaboration(collaboration_id=collaboration_id, db=db)
