from app.services.hero_certificate import *
from app.core.session import get_db
from app.api.v1.schema.hero_certificate import *
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from fastapi import APIRouter, Depends, File, Form, Query
from fastapi import UploadFile
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# ── Public read ────────────────────────────────────────────────────────────────

@router.get("/public")
async def get_public_hero_certificates_endpoint(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_public_hero_certificates(lang=lang, db=db)


# ── Admin endpoints (require JWT) ──────────────────────────────────────────────

@router.get("/all")
async def get_hero_certificates_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, le=100, description="End index (max 100)"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_hero_certificates(start=start, end=end, lang=lang, db=db)


@router.get("/{certificate_id}/admin")
async def get_hero_certificate_admin_endpoint(
    certificate_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_hero_certificate_admin(certificate_id=certificate_id, db=db)


@router.post("/create", response_model=None)
async def create_hero_certificate_endpoint(
    rank_label: str = Form(...),
    family: str = Form(...),
    issued_date: Optional[str] = Form(None),
    external_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    document: Optional[UploadFile] = File(None),
    az_title: str = Form(...),
    en_title: str = Form(...),
    az_kicker: Optional[str] = Form(None),
    en_kicker: Optional[str] = Form(None),
    az_signer: Optional[str] = Form(None),
    en_signer: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    request = HeroCertificateCreate.as_form(
        rank_label=rank_label,
        family=family,
        issued_date=issued_date,
        external_url=external_url,
        image=image,
        document=document,
        az_title=az_title,
        en_title=en_title,
        az_kicker=az_kicker,
        en_kicker=en_kicker,
        az_signer=az_signer,
        en_signer=en_signer
    )
    return await create_hero_certificate(request=request, db=db)


@router.put("/{certificate_id}/update", response_model=None)
async def update_hero_certificate_endpoint(
    certificate_id: int,
    rank_label: str = Form(...),
    family: str = Form(...),
    issued_date: Optional[str] = Form(None),
    external_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    document: Optional[UploadFile] = File(None),
    remove_image: Optional[str] = Form(None),
    remove_document: Optional[str] = Form(None),
    az_title: str = Form(...),
    en_title: str = Form(...),
    az_kicker: Optional[str] = Form(None),
    en_kicker: Optional[str] = Form(None),
    az_signer: Optional[str] = Form(None),
    en_signer: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    request = HeroCertificateUpdate.as_form(
        rank_label=rank_label,
        family=family,
        issued_date=issued_date,
        external_url=external_url,
        image=image,
        document=document,
        remove_image=remove_image,
        remove_document=remove_document,
        az_title=az_title,
        en_title=en_title,
        az_kicker=az_kicker,
        en_kicker=en_kicker,
        az_signer=az_signer,
        en_signer=en_signer
    )
    return await update_hero_certificate(certificate_id=certificate_id, request=request, db=db)


@router.post("/reorder")
async def reorder_hero_certificate_endpoint(
    request: ReOrderHeroCertificate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_hero_certificate(request=request, db=db)


@router.post("/activate")
async def activate_hero_certificate_endpoint(
    certificate_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await activate_hero_certificate(certificate_id=certificate_id, db=db)


@router.post("/deactivate")
async def deactivate_hero_certificate_endpoint(
    certificate_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await deactivate_hero_certificate(certificate_id=certificate_id, db=db)


@router.delete("/{certificate_id}/delete")
async def delete_hero_certificate_endpoint(
    certificate_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_hero_certificate(certificate_id=certificate_id, db=db)
