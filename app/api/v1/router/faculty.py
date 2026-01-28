from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.services.faculty import create_faculty, get_faculties, get_faculty, update_faculty, delete_faculty
from app.api.v1.schema.faculty import CreateFaculty, UpdateFaculty

router = APIRouter()


@router.get("/admin/all")
async def get_faculties_endpoint_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_faculties(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/public/all")
async def get_faculties_endpoint_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_faculties(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/{faculty_code}")
async def get_faculty_details_endpoint(
    faculty_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_faculty(
        faculty_code=faculty_code,
        lang_code=lang_code,
        db=db,
    )


@router.post("/create")
async def create_faculty_endpoint(
    request: CreateFaculty = Depends(CreateFaculty.as_form),
    db: AsyncSession = Depends(get_db),
):
    return await create_faculty(
        request=request,
        db=db,
    )


@router.put("/{faculty_code}")
async def update_faculty_endpoint(
    faculty_code: str,
    request: UpdateFaculty = Depends(UpdateFaculty.as_form),
    db: AsyncSession = Depends(get_db),
):
    return await update_faculty(
        faculty_code=faculty_code,
        request=request,
        db=db,
    )


@router.delete("/{faculty_code}")
async def delete_faculty_endpoint(
    faculty_code: str,
    db: AsyncSession = Depends(get_db),
):
    return await delete_faculty(
        faculty_code=faculty_code,
        db=db,
    )
