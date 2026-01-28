from app.core.session import get_db
from app.services.collaboration import *
from app.utils.language import get_language
from fastapi import APIRouter, Depends, Form
from app.api.v1.schema.collaboration import *
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/public/all")
async def get_public_collaborations_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_public_collaboration(
        start=start,
        end=end,
        lang_code=lang_code,
        db=db
    )

@router.get("/admin/all")
async def get_admin_collaborations_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    db: AsyncSession = Depends(get_db)
):
    return await get_admin_collaboration(
        start=start,
        end=end,
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

@router.post("/create")
async def create_collaboration_endpoint(
    az_title: str = Form(...),
    en_title: str = Form(...),
    image: UploadFile = File(...),
    url: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    return await create_collaboration(
        az_title=az_title,
        en_title=en_title,
        image=image,
        url=url,
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