from fastapi import UploadFile
from app.core.session import get_db
from app.api.v1.schema.project import *
from app.services.collaboration import *
from app.utils.language import get_language
from app.api.v1.schema.collabortion import *
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, Query

router = APIRouter()

@router.get("/all")
async def get_collaborations_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_collaborations(
        start=start,
        end=end,
        lang=lang,
        db=db
    )

@router.post("/create")
async def create_collaboration_endpoint(
    image: UploadFile = File(...),
    az_title: str = Form(...),
    en_title: str = Form(...),
    url: Optional[str] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_collaboration(
        image=image,
        az_title=az_title,
        en_title=en_title,
        url=url,
        db=db
    )

@router.post("/{collaboration_id}/deactivate")
async def deactivate_collaboration_endpoint(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await deactivate_collaboration(
        collaboration_id=collaboration_id,
        db=db
    )

@router.post("/{collaboration_id}/activate")
async def activate_collaboration_endpoint(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await activate_collaboration(
        collaboration_id=collaboration_id,
        db=db
    )

@router.post("/reorder")
async def reorder_collaboration_endpoint(
    request: ReOrderCollaboration,
    db: AsyncSession = Depends(get_db)
):
    return await reorder_collaboration(
        request=request,
        db=db
    )

@router.delete("/{collaboration_id}/delete")
async def delete_collaboration_endpoint(
    collaboration_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await delete_collaboration(
        collaboration_id=collaboration_id,
        db=db
    )