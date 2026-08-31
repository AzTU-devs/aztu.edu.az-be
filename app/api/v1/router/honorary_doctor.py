from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.honorary_doctor import (
    HonoraryDoctorCreate,
    HonoraryDoctorUpdate,
    ReOrderHonoraryDoctor,
)
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.honorary_doctor import (
    activate_honorary_doctor,
    create_honorary_doctor,
    deactivate_honorary_doctor,
    delete_honorary_doctor,
    get_honorary_doctor_admin,
    get_honorary_doctors,
    get_public_honorary_doctors,
    reorder_honorary_doctor,
    update_honorary_doctor,
)
from app.utils.language import get_language

router = APIRouter()


# ── Public read ────────────────────────────────────────────────────────────────

@router.get("/public")
async def get_public_honorary_doctors_endpoint(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_public_honorary_doctors(lang=lang, db=db)


# ── Admin endpoints (require JWT) ──────────────────────────────────────────────

@router.get("/all")
async def get_honorary_doctors_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(100, gt=0, le=100, description="End index (max 100)"),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_honorary_doctors(start=start, end=end, db=db)


@router.get("/{doctor_id}/admin")
async def get_honorary_doctor_admin_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_honorary_doctor_admin(doctor_id=doctor_id, db=db)


@router.post("/create", response_model=None)
async def create_honorary_doctor_endpoint(
    az_full_name: str = Form(...),
    en_full_name: str = Form(...),
    az_description: Optional[str] = Form(None),
    en_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    request = HonoraryDoctorCreate.as_form(
        az_full_name=az_full_name,
        en_full_name=en_full_name,
        az_description=az_description,
        en_description=en_description,
        image=image,
    )
    return await create_honorary_doctor(request=request, db=db)


@router.put("/{doctor_id}/update", response_model=None)
async def update_honorary_doctor_endpoint(
    doctor_id: int,
    az_full_name: str = Form(...),
    en_full_name: str = Form(...),
    az_description: Optional[str] = Form(None),
    en_description: Optional[str] = Form(None),
    remove_image: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    request = HonoraryDoctorUpdate.as_form(
        az_full_name=az_full_name,
        en_full_name=en_full_name,
        az_description=az_description,
        en_description=en_description,
        remove_image=remove_image,
        image=image,
    )
    return await update_honorary_doctor(doctor_id=doctor_id, request=request, db=db)


@router.post("/reorder")
async def reorder_honorary_doctor_endpoint(
    request: ReOrderHonoraryDoctor,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_honorary_doctor(request=request, db=db)


@router.post("/activate")
async def activate_honorary_doctor_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await activate_honorary_doctor(doctor_id=doctor_id, db=db)


@router.post("/deactivate")
async def deactivate_honorary_doctor_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await deactivate_honorary_doctor(doctor_id=doctor_id, db=db)


@router.delete("/{doctor_id}/delete")
async def delete_honorary_doctor_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_honorary_doctor(doctor_id=doctor_id, db=db)
