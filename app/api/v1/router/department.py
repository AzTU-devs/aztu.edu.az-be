from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.department import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department,
    upload_director_image,
    upload_worker_image,
)
from app.api.v1.schema.department import CreateDepartment, UpdateDepartment

router = APIRouter()


@router.get("/admin/all")
async def get_departments_admin(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await get_departments(start=start, end=end, lang=lang, db=db)


@router.get("/public/all")
async def get_departments_public(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_departments(start=start, end=end, lang=lang, db=db)


@router.get("/{department_code}")
async def get_department_details(
    department_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_department(department_code=department_code, lang_code=lang, db=db)


@router.post("/create")
async def create_department_endpoint(
    request: CreateDepartment,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await create_department(request=request, db=db)


@router.put("/{department_code}")
async def update_department_endpoint(
    department_code: str,
    request: UpdateDepartment,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await update_department(department_code=department_code, request=request, db=db)


@router.delete("/{department_code}")
async def delete_department_endpoint(
    department_code: str,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await delete_department(department_code=department_code, db=db)


@router.put("/{department_code}/director/image")
async def upload_director_image_endpoint(
    department_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_director_image(department_code=department_code, image=image, db=db)


@router.put("/workers/{worker_id}/image")
async def upload_worker_image_endpoint(
    worker_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_worker_image(worker_id=worker_id, image=image, db=db)
