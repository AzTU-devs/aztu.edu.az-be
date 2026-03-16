from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.api.v1.schema.menu import (
    CreateHeaderSection, UpdateHeaderSection,
    CreateHeaderItem, UpdateHeaderItem,
    CreateHeaderSubItem, UpdateHeaderSubItem,
    CreateFooterColumn, UpdateFooterColumn,
    CreateFooterLink, UpdateFooterLink,
    CreatePartnerLogo, UpdatePartnerLogo,
    CreateQuickIcon, UpdateQuickIcon,
    CreateSocialLink, UpdateSocialLink,
    CreateContact, UpdateContact,
    CreateQuickLeftItem, UpdateQuickLeftItem,
    CreateQuickSection, UpdateQuickSection,
    CreateQuickSectionItem, UpdateQuickSectionItem,
)
from app.services.menu import (
    get_header_menu, get_footer_menu, get_quick_menu,
    create_header_section, update_header_section, delete_header_section,
    create_header_item, update_header_item, delete_header_item,
    create_header_sub_item, update_header_sub_item, delete_header_sub_item,
    create_footer_column, update_footer_column, delete_footer_column,
    create_footer_link, update_footer_link, delete_footer_link,
    create_partner_logo, update_partner_logo, delete_partner_logo,
    create_quick_icon, update_quick_icon, delete_quick_icon,
    create_social_link, update_social_link, delete_social_link,
    create_contact, update_contact, delete_contact,
    create_quick_left_item, update_quick_left_item, delete_quick_left_item,
    create_quick_section, update_quick_section, delete_quick_section,
    create_quick_section_item, update_quick_section_item, delete_quick_section_item,
)

router = APIRouter()

# All mutation endpoints share a single auth dependency via this sub-router
admin_router = APIRouter(dependencies=[Depends(require_admin)])


# ─────────────────────────────────────────────────────────────
# GET  —  public read endpoints
# ─────────────────────────────────────────────────────────────

@router.get("/header")
async def get_header_menu_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_header_menu(lang_code=lang_code, db=db)


@router.get("/footer")
async def get_footer_menu_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_footer_menu(lang_code=lang_code, db=db)


@router.get("/quick")
async def get_quick_menu_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_quick_menu(lang_code=lang_code, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Header Section
# ─────────────────────────────────────────────────────────────

@admin_router.post("/header/section")
async def create_header_section_endpoint(
    request: CreateHeaderSection,
    db: AsyncSession = Depends(get_db),
):
    return await create_header_section(request=request, db=db)


@admin_router.put("/header/section/{section_id}")
async def update_header_section_endpoint(
    section_id: int,
    request: UpdateHeaderSection,
    db: AsyncSession = Depends(get_db),
):
    return await update_header_section(section_id=section_id, request=request, db=db)


@admin_router.delete("/header/section/{section_id}")
async def delete_header_section_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header_section(section_id=section_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Header Item
# ─────────────────────────────────────────────────────────────

@admin_router.post("/header/item")
async def create_header_item_endpoint(
    request: CreateHeaderItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_header_item(request=request, db=db)


@admin_router.put("/header/item/{item_id}")
async def update_header_item_endpoint(
    item_id: int,
    request: UpdateHeaderItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_header_item(item_id=item_id, request=request, db=db)


@admin_router.delete("/header/item/{item_id}")
async def delete_header_item_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header_item(item_id=item_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Header Sub-Item
# ─────────────────────────────────────────────────────────────

@admin_router.post("/header/sub-item")
async def create_header_sub_item_endpoint(
    request: CreateHeaderSubItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_header_sub_item(request=request, db=db)


@admin_router.put("/header/sub-item/{sub_item_id}")
async def update_header_sub_item_endpoint(
    sub_item_id: int,
    request: UpdateHeaderSubItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_header_sub_item(sub_item_id=sub_item_id, request=request, db=db)


@admin_router.delete("/header/sub-item/{sub_item_id}")
async def delete_header_sub_item_endpoint(
    sub_item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header_sub_item(sub_item_id=sub_item_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Column
# ─────────────────────────────────────────────────────────────

@admin_router.post("/footer/column")
async def create_footer_column_endpoint(
    request: CreateFooterColumn,
    db: AsyncSession = Depends(get_db),
):
    return await create_footer_column(request=request, db=db)


@admin_router.put("/footer/column/{column_id}")
async def update_footer_column_endpoint(
    column_id: int,
    request: UpdateFooterColumn,
    db: AsyncSession = Depends(get_db),
):
    return await update_footer_column(column_id=column_id, request=request, db=db)


@admin_router.delete("/footer/column/{column_id}")
async def delete_footer_column_endpoint(
    column_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_footer_column(column_id=column_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Link
# ─────────────────────────────────────────────────────────────

@admin_router.post("/footer/link")
async def create_footer_link_endpoint(
    request: CreateFooterLink,
    db: AsyncSession = Depends(get_db),
):
    return await create_footer_link(request=request, db=db)


@admin_router.put("/footer/link/{link_id}")
async def update_footer_link_endpoint(
    link_id: int,
    request: UpdateFooterLink,
    db: AsyncSession = Depends(get_db),
):
    return await update_footer_link(link_id=link_id, request=request, db=db)


@admin_router.delete("/footer/link/{link_id}")
async def delete_footer_link_endpoint(
    link_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_footer_link(link_id=link_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Partner Logo
# ─────────────────────────────────────────────────────────────

@admin_router.post("/footer/partner-logo")
async def create_partner_logo_endpoint(
    request: CreatePartnerLogo,
    db: AsyncSession = Depends(get_db),
):
    return await create_partner_logo(request=request, db=db)


@admin_router.put("/footer/partner-logo/{logo_id}")
async def update_partner_logo_endpoint(
    logo_id: int,
    request: UpdatePartnerLogo,
    db: AsyncSession = Depends(get_db),
):
    return await update_partner_logo(logo_id=logo_id, request=request, db=db)


@admin_router.delete("/footer/partner-logo/{logo_id}")
async def delete_partner_logo_endpoint(
    logo_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_partner_logo(logo_id=logo_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Quick Icon
# ─────────────────────────────────────────────────────────────

@admin_router.post("/footer/quick-icon")
async def create_quick_icon_endpoint(
    request: CreateQuickIcon,
    db: AsyncSession = Depends(get_db),
):
    return await create_quick_icon(request=request, db=db)


@admin_router.put("/footer/quick-icon/{icon_id}")
async def update_quick_icon_endpoint(
    icon_id: int,
    request: UpdateQuickIcon,
    db: AsyncSession = Depends(get_db),
):
    return await update_quick_icon(icon_id=icon_id, request=request, db=db)


@admin_router.delete("/footer/quick-icon/{icon_id}")
async def delete_quick_icon_endpoint(
    icon_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_quick_icon(icon_id=icon_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Social Link
# ─────────────────────────────────────────────────────────────

@admin_router.post("/social-link")
async def create_social_link_endpoint(
    request: CreateSocialLink,
    db: AsyncSession = Depends(get_db),
):
    return await create_social_link(request=request, db=db)


@admin_router.put("/social-link/{link_id}")
async def update_social_link_endpoint(
    link_id: int,
    request: UpdateSocialLink,
    db: AsyncSession = Depends(get_db),
):
    return await update_social_link(link_id=link_id, request=request, db=db)


@admin_router.delete("/social-link/{link_id}")
async def delete_social_link_endpoint(
    link_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_social_link(link_id=link_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Contact
# ─────────────────────────────────────────────────────────────

@admin_router.post("/contact")
async def create_contact_endpoint(
    request: CreateContact,
    db: AsyncSession = Depends(get_db),
):
    return await create_contact(request=request, db=db)


@admin_router.put("/contact/{contact_id}")
async def update_contact_endpoint(
    contact_id: int,
    request: UpdateContact,
    db: AsyncSession = Depends(get_db),
):
    return await update_contact(contact_id=contact_id, request=request, db=db)


@admin_router.delete("/contact/{contact_id}")
async def delete_contact_endpoint(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_contact(contact_id=contact_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Left Item
# ─────────────────────────────────────────────────────────────

@admin_router.post("/quick/left-item")
async def create_quick_left_item_endpoint(
    request: CreateQuickLeftItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_quick_left_item(request=request, db=db)


@admin_router.put("/quick/left-item/{item_id}")
async def update_quick_left_item_endpoint(
    item_id: int,
    request: UpdateQuickLeftItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_quick_left_item(item_id=item_id, request=request, db=db)


@admin_router.delete("/quick/left-item/{item_id}")
async def delete_quick_left_item_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_quick_left_item(item_id=item_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Section
# ─────────────────────────────────────────────────────────────

@admin_router.post("/quick/section")
async def create_quick_section_endpoint(
    request: CreateQuickSection,
    db: AsyncSession = Depends(get_db),
):
    return await create_quick_section(request=request, db=db)


@admin_router.put("/quick/section/{section_id}")
async def update_quick_section_endpoint(
    section_id: int,
    request: UpdateQuickSection,
    db: AsyncSession = Depends(get_db),
):
    return await update_quick_section(section_id=section_id, request=request, db=db)


@admin_router.delete("/quick/section/{section_id}")
async def delete_quick_section_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_quick_section(section_id=section_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Section Item
# ─────────────────────────────────────────────────────────────

@admin_router.post("/quick/section-item")
async def create_quick_section_item_endpoint(
    request: CreateQuickSectionItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_quick_section_item(request=request, db=db)


@admin_router.put("/quick/section-item/{item_id}")
async def update_quick_section_item_endpoint(
    item_id: int,
    request: UpdateQuickSectionItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_quick_section_item(item_id=item_id, request=request, db=db)


@admin_router.delete("/quick/section-item/{item_id}")
async def delete_quick_section_item_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_quick_section_item(item_id=item_id, db=db)


# Merge admin mutations into the public router so main.py only imports `router`
router.include_router(admin_router)
