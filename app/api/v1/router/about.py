from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.about import (
    CreateAboutItem,
    CreateAboutPage,
    CreateAboutPerson,
    CreateAboutSection,
    PublishAboutPage,
    ReorderPayload,
    UpdateAboutItem,
    UpdateAboutPage,
    UpdateAboutPerson,
    UpdateAboutSection,
)
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.about import (
    create_item,
    create_page,
    create_person,
    create_section,
    delete_item,
    delete_page,
    delete_person,
    delete_section,
    get_page_admin,
    get_page_public,
    get_pages_admin,
    get_pages_public,
    publish_page,
    reorder_items,
    reorder_people,
    reorder_sections,
    update_item,
    update_page,
    update_person,
    update_section,
    upload_item_file,
    upload_item_image,
    upload_page_file,
    upload_page_image,
    upload_person_image,
)
from app.utils.language import get_language

router = APIRouter()


# ── Admin reads ────────────────────────────────────────────────────────────────


@router.get("/admin/pages")
async def list_pages_admin(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_pages_admin(db=db, lang=lang)


@router.get("/admin/pages/{page_key}")
async def read_page_admin(
    page_key: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_page_admin(page_key=page_key, db=db)


# ── Public reads ───────────────────────────────────────────────────────────────


@router.get("/public/pages")
async def list_pages_public(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_pages_public(lang=lang, db=db)


@router.get("/public/pages/{page_key}")
async def read_page_public(
    page_key: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_page_public(page_key=page_key, lang=lang, db=db)


# ── Pages ──────────────────────────────────────────────────────────────────────


@router.post("/admin/pages")
async def create_page_endpoint(
    request: CreateAboutPage,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_page(request=request, db=db)


@router.put("/admin/pages/{page_key}")
async def update_page_endpoint(
    page_key: str,
    request: UpdateAboutPage,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_page(page_key=page_key, request=request, db=db)


@router.put("/admin/pages/{page_key}/publish")
async def publish_page_endpoint(
    page_key: str,
    request: PublishAboutPage,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await publish_page(page_key=page_key, is_active=request.is_active, db=db)


@router.delete("/admin/pages/{page_key}")
async def delete_page_endpoint(
    page_key: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_page(page_key=page_key, db=db)


@router.put("/admin/pages/{page_key}/image")
async def upload_page_image_endpoint(
    page_key: str,
    field: str = Form("hero_image"),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_page_image(page_key=page_key, field=field, image=image, db=db)


@router.put("/admin/pages/{page_key}/file")
async def upload_page_file_endpoint(
    page_key: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_page_file(page_key=page_key, file=file, db=db)


# ── Sections ───────────────────────────────────────────────────────────────────


@router.post("/admin/pages/{page_key}/sections")
async def create_section_endpoint(
    page_key: str,
    request: CreateAboutSection,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_section(page_key=page_key, request=request, db=db)


@router.put("/admin/pages/{page_key}/sections/order")
async def reorder_sections_endpoint(
    page_key: str,
    request: ReorderPayload,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_sections(page_key=page_key, payload=request, db=db)


@router.put("/admin/sections/{section_id}")
async def update_section_endpoint(
    section_id: int,
    request: UpdateAboutSection,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_section(section_id=section_id, request=request, db=db)


@router.delete("/admin/sections/{section_id}")
async def delete_section_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_section(section_id=section_id, db=db)


# ── Items ──────────────────────────────────────────────────────────────────────


@router.post("/admin/sections/{section_id}/items")
async def create_item_endpoint(
    section_id: int,
    request: CreateAboutItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_item(section_id=section_id, request=request, db=db)


@router.put("/admin/sections/{section_id}/items/order")
async def reorder_items_endpoint(
    section_id: int,
    request: ReorderPayload,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_items(section_id=section_id, payload=request, db=db)


@router.put("/admin/items/{item_id}")
async def update_item_endpoint(
    item_id: int,
    request: UpdateAboutItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_item(item_id=item_id, request=request, db=db)


@router.delete("/admin/items/{item_id}")
async def delete_item_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_item(item_id=item_id, db=db)


@router.put("/admin/items/{item_id}/image")
async def upload_item_image_endpoint(
    item_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_item_image(item_id=item_id, image=image, db=db)


@router.put("/admin/items/{item_id}/file")
async def upload_item_file_endpoint(
    item_id: int,
    file: UploadFile = File(...),
    lang: Optional[str] = Query(None, description="az | en for a per-language file"),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_item_file(item_id=item_id, lang=lang, file=file, db=db)


# ── People ─────────────────────────────────────────────────────────────────────


@router.post("/admin/sections/{section_id}/people")
async def create_person_endpoint(
    section_id: int,
    request: CreateAboutPerson,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_person(section_id=section_id, request=request, db=db)


@router.put("/admin/sections/{section_id}/people/order")
async def reorder_people_endpoint(
    section_id: int,
    request: ReorderPayload,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_people(section_id=section_id, payload=request, db=db)


@router.put("/admin/people/{person_id}")
async def update_person_endpoint(
    person_id: int,
    request: UpdateAboutPerson,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_person(person_id=person_id, request=request, db=db)


@router.delete("/admin/people/{person_id}")
async def delete_person_endpoint(
    person_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_person(person_id=person_id, db=db)


@router.put("/admin/people/{person_id}/image")
async def upload_person_image_endpoint(
    person_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_person_image(person_id=person_id, image=image, db=db)
