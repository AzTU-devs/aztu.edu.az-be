from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.research_institute import (
    create_research_institute,
    get_research_institutes,
    get_research_institute,
    update_research_institute,
    delete_research_institute,
    upload_institute_image,
    upload_director_image,
    upload_staff_image,
)
from app.api.v1.schema.research_institute import CreateResearchInstitute, UpdateResearchInstitute

router = APIRouter()


@router.get("/admin/all")
async def get_institutes_admin(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_research_institutes(start=start, end=end, lang=lang, db=db)


@router.get("/public/all")
async def get_institutes_public(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_institutes(start=start, end=end, lang=lang, db=db)


@router.get("/{institute_code}")
async def get_institute_details(
    institute_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_institute(institute_code=institute_code, lang_code=lang, db=db)


@router.post("/create")
async def create_institute_endpoint(
    request: CreateResearchInstitute,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_research_institute(request=request, db=db)


@router.put("/{institute_code}")
async def update_institute_endpoint(
    institute_code: str,
    request: UpdateResearchInstitute,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_research_institute(institute_code=institute_code, request=request, db=db)


@router.delete("/{institute_code}")
async def delete_institute_endpoint(
    institute_code: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_research_institute(institute_code=institute_code, db=db)


@router.put("/{institute_code}/image")
async def upload_institute_image_endpoint(
    institute_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_institute_image(institute_code=institute_code, image=image, db=db)


@router.put("/{institute_code}/director/image")
async def upload_director_image_endpoint(
    institute_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_director_image(institute_code=institute_code, image=image, db=db)


@router.put("/staff/{staff_id}/image")
async def upload_staff_image_endpoint(
    staff_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_staff_image(staff_id=staff_id, image=image, db=db)
