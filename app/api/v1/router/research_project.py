from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.research_project import (
    create_research_project,
    get_research_projects,
    get_research_project,
    get_research_project_admin,
    update_research_project,
    delete_research_project,
    upload_project_image,
)
from app.api.v1.schema.research_project import CreateResearchProject, UpdateResearchProject

router = APIRouter()


@router.get("/admin/all")
async def get_projects_admin(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_research_projects(start=start, end=end, lang=lang, db=db)


@router.get("/admin/{project_code}")
async def get_project_admin(
    project_code: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_research_project_admin(project_code=project_code, db=db)


@router.get("/public/all")
async def get_projects_public(
    start: int = Query(0, ge=0),
    end: int = Query(50, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_projects(start=start, end=end, lang=lang, db=db)


@router.get("/{project_code}")
async def get_project_details(
    project_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_project(project_code=project_code, lang_code=lang, db=db)


@router.post("/create")
async def create_project_endpoint(
    request: CreateResearchProject,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_research_project(request=request, db=db)


@router.put("/{project_code}")
async def update_project_endpoint(
    project_code: str,
    request: UpdateResearchProject,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_research_project(project_code=project_code, request=request, db=db)


@router.delete("/{project_code}")
async def delete_project_endpoint(
    project_code: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_research_project(project_code=project_code, db=db)


@router.put("/{project_code}/image")
async def upload_project_image_endpoint(
    project_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_project_image(project_code=project_code, image=image, db=db)
