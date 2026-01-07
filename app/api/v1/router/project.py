from app.services.project import *
from app.core.session import get_db
from app.api.v1.schema.project import *
from app.utils.language import get_language
from fastapi import APIRouter, Depends, File, Form, Query
from fastapi import Body
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/all")
async def get_projects_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_projects(
        start=start,
        end=end,
        lang=lang,
        db=db
    )

@router.get("/{project_id}")
async def get_project_by_id_endpoint(
    project_id: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_project_by_id(
        project_id=project_id,
        lang=lang,
        db=db
    )

@router.post("/create", response_model=None)
async def create_project_endpoint(
    bg_image: UploadFile = File(...),
    az_title: str = Form(...),
    az_desc: str = Form(...),
    az_content_html: str = Form(...),
    en_title: str = Form(...),
    en_desc: str = Form(...),
    en_content_html: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    project = ProjectCreate.as_form(
        bg_image=bg_image,
        az_title=az_title,
        az_desc=az_desc,
        az_content_html=az_content_html,
        en_title=en_title,
        en_desc=en_desc,
        en_content_html=en_content_html
    )
    return await create_project(request=project, db=db)


@router.post("/reorder")
async def reorder_project_endpoint(
    request: ReOrderProject,
    db: AsyncSession = Depends(get_db),
):
    return await reorder_project(
        request=request,
        db=db
    )

@router.delete("/{project_id}/delete")
async def delete_project_endpoint(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await delete_project(
        project_id=project_id,
        db=db
    )