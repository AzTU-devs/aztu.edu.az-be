from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.api.v1.schema.research_institute import (
    CreateResearchInstitute,
    UpdateResearchInstitute,
)
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

router = APIRouter()


@router.get("/admin/all")
async def get_research_institutes_endpoint_admin(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_institutes(start=start, end=end, lang=lang, db=db)


@router.get("/public/all")
async def get_research_institutes_endpoint_public(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_institutes(start=start, end=end, lang=lang, db=db)


@router.get("/{institute_code}")
async def get_research_institute_endpoint(
    institute_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_research_institute(institute_code=institute_code, lang=lang, db=db)


@router.post("/create")
async def create_research_institute_endpoint(
    request: CreateResearchInstitute,
    db: AsyncSession = Depends(get_db),
):
    return await create_research_institute(request=request, db=db)


@router.patch("/{institute_code}")
async def update_research_institute_endpoint(
    institute_code: str,
    request: UpdateResearchInstitute,
    db: AsyncSession = Depends(get_db),
):
    return await update_research_institute(institute_code=institute_code, request=request, db=db)


@router.delete("/{institute_code}")
async def delete_research_institute_endpoint(
    institute_code: str,
    db: AsyncSession = Depends(get_db),
):
    return await delete_research_institute(institute_code=institute_code, db=db)


@router.put("/{institute_code}/image")
async def upload_institute_image_endpoint(
    institute_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await upload_institute_image(institute_code=institute_code, image=image, db=db)


@router.put("/director/{director_id}/image")
async def upload_director_image_endpoint(
    director_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await upload_director_image(director_id=director_id, image=image, db=db)


@router.put("/staff/{staff_id}/image")
async def upload_staff_image_endpoint(
    staff_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await upload_staff_image(staff_id=staff_id, image=image, db=db)
