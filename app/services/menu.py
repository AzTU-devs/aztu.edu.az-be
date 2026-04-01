from typing import Optional
from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.responses import JSONResponse
from app.core.logger import get_logger
from app.utils.file_upload import safe_delete_file

logger = get_logger(__name__)

from app.models.menu.footer import (
    MenuFooterColumn, MenuFooterColumnTranslation,
    MenuFooterLink, MenuFooterLinkTranslation,
    MenuFooterPartnerLogo, MenuFooterQuickIcon, MenuFooterQuickIconTranslation,
)
from app.models.menu.shared import (
    MenuSocialLink, MenuContact, MenuContactPhone, MenuContactAddress,
)
from app.models.menu.quick import (
    MenuQuickLeftItem, MenuQuickLeftItemTranslation,
    MenuQuickSection, MenuQuickSectionTranslation,
    MenuQuickSectionItem, MenuQuickSectionItemTranslation,
)
from app.api.v1.schema.menu import (
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

LANGS = ("az", "en")


# ─────────────────────────────────────────────────────────────
# GET  —  Footer
# ─────────────────────────────────────────────────────────────

async def get_footer_menu(lang_code: str, db: AsyncSession):
    try:
        columns_result = await db.execute(
            select(MenuFooterColumn)
            .where(MenuFooterColumn.is_active == True)
            .order_by(MenuFooterColumn.display_order.asc())
        )
        columns = columns_result.scalars().all()

        columns_arr = []
        for column in columns:
            col_tr_result = await db.execute(
                select(MenuFooterColumnTranslation).where(
                    MenuFooterColumnTranslation.column_id == column.id,
                    MenuFooterColumnTranslation.lang_code == lang_code,
                )
            )
            col_tr = col_tr_result.scalar_one_or_none()
            if not col_tr:
                continue

            links_result = await db.execute(
                select(MenuFooterLink)
                .where(
                    MenuFooterLink.column_id == column.id,
                    MenuFooterLink.is_active == True,
                )
                .order_by(MenuFooterLink.display_order.asc())
            )
            links = links_result.scalars().all()

            links_arr = []
            for link in links:
                link_tr_result = await db.execute(
                    select(MenuFooterLinkTranslation).where(
                        MenuFooterLinkTranslation.link_id == link.id,
                        MenuFooterLinkTranslation.lang_code == lang_code,
                    )
                )
                link_tr = link_tr_result.scalar_one_or_none()
                if not link_tr:
                    continue
                links_arr.append({"label": link_tr.label, "url": link.url})

            columns_arr.append({"title": col_tr.title, "links": links_arr})

        contact_result = await db.execute(
            select(MenuContact).where(
                MenuContact.context == "footer",
                MenuContact.is_active == True,
            )
        )
        contact = contact_result.scalar_one_or_none()

        contact_obj = {}
        if contact:
            phones_result = await db.execute(
                select(MenuContactPhone)
                .where(MenuContactPhone.contact_id == contact.id)
                .order_by(MenuContactPhone.display_order.asc())
            )
            phones = phones_result.scalars().all()

            address_result = await db.execute(
                select(MenuContactAddress).where(
                    MenuContactAddress.contact_id == contact.id,
                    MenuContactAddress.lang_code == lang_code,
                )
            )
            address = address_result.scalar_one_or_none()
            contact_obj = {
                "email": contact.email,
                "phones": [p.phone for p in phones],
                "address": address.address if address else "",
            }

        social_result = await db.execute(
            select(MenuSocialLink)
            .where(
                MenuSocialLink.context.in_(["footer", "both"]),
                MenuSocialLink.is_active == True,
            )
            .order_by(MenuSocialLink.display_order.asc())
        )
        social_arr = [
            {"platform": s.platform, "url": s.url}
            for s in social_result.scalars().all()
        ]

        logos_result = await db.execute(
            select(MenuFooterPartnerLogo)
            .where(MenuFooterPartnerLogo.is_active == True)
            .order_by(MenuFooterPartnerLogo.display_order.asc())
        )
        logos_arr = [
            {"label": l.label, "image_url": l.image_url, "url": l.url}
            for l in logos_result.scalars().all()
        ]

        icons_result = await db.execute(
            select(MenuFooterQuickIcon)
            .where(MenuFooterQuickIcon.is_active == True)
            .order_by(MenuFooterQuickIcon.display_order.asc())
        )
        icons_arr = []
        for icon in icons_result.scalars().all():
            icon_tr_result = await db.execute(
                select(MenuFooterQuickIconTranslation).where(
                    MenuFooterQuickIconTranslation.icon_id == icon.id,
                    MenuFooterQuickIconTranslation.lang_code == lang_code,
                )
            )
            icon_tr = icon_tr_result.scalar_one_or_none()
            if not icon_tr:
                continue
            icons_arr.append({"label": icon_tr.label, "icon": icon.icon, "url": icon.url})

        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "university_name": "Azerbaijan Technical University",
                    "columns": columns_arr,
                    "contact": contact_obj,
                    "social_links": social_arr,
                    "partner_logos": logos_arr,
                    "quick_icons": icons_arr,
                },
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# GET  —  Quick
# ─────────────────────────────────────────────────────────────

async def get_quick_menu(lang_code: str, db: AsyncSession):
    try:
        left_items_result = await db.execute(
            select(MenuQuickLeftItem)
            .where(MenuQuickLeftItem.is_active == True)
            .order_by(MenuQuickLeftItem.display_order.asc())
        )
        left_items_arr = []
        for item in left_items_result.scalars().all():
            item_tr_result = await db.execute(
                select(MenuQuickLeftItemTranslation).where(
                    MenuQuickLeftItemTranslation.item_id == item.id,
                    MenuQuickLeftItemTranslation.lang_code == lang_code,
                )
            )
            item_tr = item_tr_result.scalar_one_or_none()
            if not item_tr:
                continue
            left_items_arr.append({"label": item_tr.label, "url": item.url})

        contact_result = await db.execute(
            select(MenuContact).where(
                MenuContact.context == "quick",
                MenuContact.is_active == True,
            )
        )
        contact = contact_result.scalar_one_or_none()
        contact_obj = {}
        if contact:
            phones_result = await db.execute(
                select(MenuContactPhone)
                .where(MenuContactPhone.contact_id == contact.id)
                .order_by(MenuContactPhone.display_order.asc())
            )
            contact_obj = {
                "email": contact.email,
                "phones": [p.phone for p in phones_result.scalars().all()],
            }

        social_result = await db.execute(
            select(MenuSocialLink)
            .where(
                MenuSocialLink.context.in_(["quick", "both"]),
                MenuSocialLink.is_active == True,
            )
            .order_by(MenuSocialLink.display_order.asc())
        )
        social_arr = [
            {"platform": s.platform, "url": s.url}
            for s in social_result.scalars().all()
        ]

        sections_result = await db.execute(
            select(MenuQuickSection)
            .where(MenuQuickSection.is_active == True)
            .order_by(MenuQuickSection.display_order.asc())
        )
        sections_arr = []
        for section in sections_result.scalars().all():
            section_tr_result = await db.execute(
                select(MenuQuickSectionTranslation).where(
                    MenuQuickSectionTranslation.section_id == section.id,
                    MenuQuickSectionTranslation.lang_code == lang_code,
                )
            )
            section_tr = section_tr_result.scalar_one_or_none()
            if not section_tr:
                continue

            items_result = await db.execute(
                select(MenuQuickSectionItem)
                .where(
                    MenuQuickSectionItem.section_id == section.id,
                    MenuQuickSectionItem.is_active == True,
                )
                .order_by(MenuQuickSectionItem.display_order.asc())
            )
            items_arr = []
            for item in items_result.scalars().all():
                item_tr_result = await db.execute(
                    select(MenuQuickSectionItemTranslation).where(
                        MenuQuickSectionItemTranslation.item_id == item.id,
                        MenuQuickSectionItemTranslation.lang_code == lang_code,
                    )
                )
                item_tr = item_tr_result.scalar_one_or_none()
                if not item_tr:
                    continue
                items_arr.append({"label": item_tr.label, "url": item.url})

            sections_arr.append({
                "key": section.section_key,
                "title": section_tr.title,
                "items": items_arr,
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "title": "AzTU Quick Menu",
                    "left_items": left_items_arr,
                    "contact": contact_obj,
                    "social_links": social_arr,
                    "right_sections": sections_arr,
                },
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Column
# ─────────────────────────────────────────────────────────────

async def create_footer_column(request: CreateFooterColumn, db: AsyncSession):
    try:
        column = MenuFooterColumn(display_order=request.display_order)
        db.add(column)
        await db.flush()

        for lang in LANGS:
            db.add(MenuFooterColumnTranslation(
                column_id=column.id,
                lang_code=lang,
                title=getattr(request.title, lang),
            ))

        await db.commit()
        await db.refresh(column)
        return JSONResponse(
            content={"status_code": 201, "message": "Footer column created.", "id": column.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_footer_column(column_id: int, request: UpdateFooterColumn, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterColumn).where(MenuFooterColumn.id == column_id)
        )
        column = result.scalar_one_or_none()
        if not column:
            return JSONResponse(
                content={"status_code": 404, "message": "Column not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.display_order is not None:
            column.display_order = request.display_order

        if request.title:
            for lang in LANGS:
                val = getattr(request.title, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuFooterColumnTranslation).where(
                        MenuFooterColumnTranslation.column_id == column_id,
                        MenuFooterColumnTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.title = val
                else:
                    db.add(MenuFooterColumnTranslation(column_id=column_id, lang_code=lang, title=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Footer column updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_footer_column(column_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterColumn).where(MenuFooterColumn.id == column_id)
        )
        column = result.scalar_one_or_none()
        if not column:
            return JSONResponse(
                content={"status_code": 404, "message": "Column not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(column)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Footer column deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Link
# ─────────────────────────────────────────────────────────────

async def create_footer_link(request: CreateFooterLink, db: AsyncSession):
    try:
        column_check = await db.execute(
            select(MenuFooterColumn).where(MenuFooterColumn.id == request.column_id)
        )
        if not column_check.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Column not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        link = MenuFooterLink(
            column_id=request.column_id,
            url=request.url,
            display_order=request.display_order,
        )
        db.add(link)
        await db.flush()

        for lang in LANGS:
            db.add(MenuFooterLinkTranslation(
                link_id=link.id,
                lang_code=lang,
                label=getattr(request.label, lang),
            ))

        await db.commit()
        await db.refresh(link)
        return JSONResponse(
            content={"status_code": 201, "message": "Footer link created.", "id": link.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_footer_link(link_id: int, request: UpdateFooterLink, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterLink).where(MenuFooterLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        if not link:
            return JSONResponse(
                content={"status_code": 404, "message": "Link not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.url is not None:
            link.url = request.url
        if request.display_order is not None:
            link.display_order = request.display_order

        if request.label:
            for lang in LANGS:
                val = getattr(request.label, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuFooterLinkTranslation).where(
                        MenuFooterLinkTranslation.link_id == link_id,
                        MenuFooterLinkTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.label = val
                else:
                    db.add(MenuFooterLinkTranslation(link_id=link_id, lang_code=lang, label=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Footer link updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_footer_link(link_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterLink).where(MenuFooterLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        if not link:
            return JSONResponse(
                content={"status_code": 404, "message": "Link not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(link)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Footer link deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Partner Logo
# ─────────────────────────────────────────────────────────────

async def create_partner_logo(request: CreatePartnerLogo, db: AsyncSession):
    try:
        logo = MenuFooterPartnerLogo(
            label=request.label,
            image_url=request.image_url,
            url=request.url,
            display_order=request.display_order,
        )
        db.add(logo)
        await db.commit()
        await db.refresh(logo)
        return JSONResponse(
            content={"status_code": 201, "message": "Partner logo created.", "id": logo.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_partner_logo(logo_id: int, request: UpdatePartnerLogo, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterPartnerLogo).where(MenuFooterPartnerLogo.id == logo_id)
        )
        logo = result.scalar_one_or_none()
        if not logo:
            return JSONResponse(
                content={"status_code": 404, "message": "Partner logo not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.label is not None:
            logo.label = request.label
        if request.image_url is not None:
            logo.image_url = request.image_url
        if request.url is not None:
            logo.url = request.url
        if request.display_order is not None:
            logo.display_order = request.display_order

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Partner logo updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_partner_logo(logo_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterPartnerLogo).where(MenuFooterPartnerLogo.id == logo_id)
        )
        logo = result.scalar_one_or_none()
        if not logo:
            return JSONResponse(
                content={"status_code": 404, "message": "Partner logo not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(logo)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Partner logo deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Footer Quick Icon
# ─────────────────────────────────────────────────────────────

async def create_quick_icon(request: CreateQuickIcon, db: AsyncSession):
    try:
        icon = MenuFooterQuickIcon(
            icon=request.icon,
            url=request.url,
            display_order=request.display_order,
        )
        db.add(icon)
        await db.flush()

        for lang in LANGS:
            db.add(MenuFooterQuickIconTranslation(
                icon_id=icon.id,
                lang_code=lang,
                label=getattr(request.label, lang),
            ))

        await db.commit()
        await db.refresh(icon)
        return JSONResponse(
            content={"status_code": 201, "message": "Quick icon created.", "id": icon.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_quick_icon(icon_id: int, request: UpdateQuickIcon, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterQuickIcon).where(MenuFooterQuickIcon.id == icon_id)
        )
        icon = result.scalar_one_or_none()
        if not icon:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick icon not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.icon is not None:
            icon.icon = request.icon
        if request.url is not None:
            icon.url = request.url
        if request.display_order is not None:
            icon.display_order = request.display_order

        if request.label:
            for lang in LANGS:
                val = getattr(request.label, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuFooterQuickIconTranslation).where(
                        MenuFooterQuickIconTranslation.icon_id == icon_id,
                        MenuFooterQuickIconTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.label = val
                else:
                    db.add(MenuFooterQuickIconTranslation(icon_id=icon_id, lang_code=lang, label=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick icon updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_quick_icon(icon_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuFooterQuickIcon).where(MenuFooterQuickIcon.id == icon_id)
        )
        icon = result.scalar_one_or_none()
        if not icon:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick icon not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(icon)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick icon deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Social Link
# ─────────────────────────────────────────────────────────────

async def create_social_link(request: CreateSocialLink, db: AsyncSession):
    try:
        if request.context not in ("footer", "quick", "both"):
            return JSONResponse(
                content={"status_code": 400, "message": "context must be 'footer', 'quick', or 'both'."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        link = MenuSocialLink(
            platform=request.platform,
            url=request.url,
            context=request.context,
            display_order=request.display_order,
        )
        db.add(link)
        await db.commit()
        await db.refresh(link)
        return JSONResponse(
            content={"status_code": 201, "message": "Social link created.", "id": link.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_social_link(link_id: int, request: UpdateSocialLink, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuSocialLink).where(MenuSocialLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        if not link:
            return JSONResponse(
                content={"status_code": 404, "message": "Social link not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.context is not None and request.context not in ("footer", "quick", "both"):
            return JSONResponse(
                content={"status_code": 400, "message": "context must be 'footer', 'quick', or 'both'."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if request.platform is not None:
            link.platform = request.platform
        if request.url is not None:
            link.url = request.url
        if request.context is not None:
            link.context = request.context
        if request.display_order is not None:
            link.display_order = request.display_order

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Social link updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_social_link(link_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuSocialLink).where(MenuSocialLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        if not link:
            return JSONResponse(
                content={"status_code": 404, "message": "Social link not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(link)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Social link deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Contact
# ─────────────────────────────────────────────────────────────

async def create_contact(request: CreateContact, db: AsyncSession):
    try:
        if request.context not in ("footer", "quick"):
            return JSONResponse(
                content={"status_code": 400, "message": "context must be 'footer' or 'quick'."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        contact = MenuContact(context=request.context, email=request.email)
        db.add(contact)
        await db.flush()

        for i, phone in enumerate(request.phones, start=1):
            db.add(MenuContactPhone(contact_id=contact.id, phone=phone, display_order=i))

        if request.address:
            for lang in LANGS:
                val = getattr(request.address, lang, None)
                if val:
                    db.add(MenuContactAddress(contact_id=contact.id, lang_code=lang, address=val))

        await db.commit()
        await db.refresh(contact)
        return JSONResponse(
            content={"status_code": 201, "message": "Contact created.", "id": contact.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_contact(contact_id: int, request: UpdateContact, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuContact).where(MenuContact.id == contact_id)
        )
        contact = result.scalar_one_or_none()
        if not contact:
            return JSONResponse(
                content={"status_code": 404, "message": "Contact not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.email is not None:
            contact.email = request.email

        if request.phones is not None:
            await db.execute(
                sql_delete(MenuContactPhone).where(MenuContactPhone.contact_id == contact_id)
            )
            for i, phone in enumerate(request.phones, start=1):
                db.add(MenuContactPhone(contact_id=contact_id, phone=phone, display_order=i))

        if request.address:
            for lang in LANGS:
                val = getattr(request.address, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuContactAddress).where(
                        MenuContactAddress.contact_id == contact_id,
                        MenuContactAddress.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.address = val
                else:
                    db.add(MenuContactAddress(contact_id=contact_id, lang_code=lang, address=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Contact updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_contact(contact_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuContact).where(MenuContact.id == contact_id)
        )
        contact = result.scalar_one_or_none()
        if not contact:
            return JSONResponse(
                content={"status_code": 404, "message": "Contact not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(contact)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Contact deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Left Item
# ─────────────────────────────────────────────────────────────

async def create_quick_left_item(request: CreateQuickLeftItem, db: AsyncSession):
    try:
        item = MenuQuickLeftItem(url=request.url, display_order=request.display_order)
        db.add(item)
        await db.flush()

        for lang in LANGS:
            db.add(MenuQuickLeftItemTranslation(
                item_id=item.id,
                lang_code=lang,
                label=getattr(request.label, lang),
            ))

        await db.commit()
        await db.refresh(item)
        return JSONResponse(
            content={"status_code": 201, "message": "Quick left item created.", "id": item.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_quick_left_item(item_id: int, request: UpdateQuickLeftItem, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickLeftItem).where(MenuQuickLeftItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick left item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.url is not None:
            item.url = request.url
        if request.display_order is not None:
            item.display_order = request.display_order

        if request.label:
            for lang in LANGS:
                val = getattr(request.label, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuQuickLeftItemTranslation).where(
                        MenuQuickLeftItemTranslation.item_id == item_id,
                        MenuQuickLeftItemTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.label = val
                else:
                    db.add(MenuQuickLeftItemTranslation(item_id=item_id, lang_code=lang, label=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick left item updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_quick_left_item(item_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickLeftItem).where(MenuQuickLeftItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick left item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(item)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick left item deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Section
# ─────────────────────────────────────────────────────────────

async def create_quick_section(request: CreateQuickSection, db: AsyncSession):
    try:
        existing = await db.execute(
            select(MenuQuickSection).where(MenuQuickSection.section_key == request.section_key)
        )
        if existing.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 409, "message": "Section key already exists."},
                status_code=status.HTTP_409_CONFLICT,
            )

        section = MenuQuickSection(
            section_key=request.section_key,
            display_order=request.display_order,
        )
        db.add(section)
        await db.flush()

        for lang in LANGS:
            db.add(MenuQuickSectionTranslation(
                section_id=section.id,
                lang_code=lang,
                title=getattr(request.title, lang),
            ))

        await db.commit()
        await db.refresh(section)
        return JSONResponse(
            content={"status_code": 201, "message": "Quick section created.", "id": section.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_quick_section(section_id: int, request: UpdateQuickSection, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickSection).where(MenuQuickSection.id == section_id)
        )
        section = result.scalar_one_or_none()
        if not section:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick section not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.display_order is not None:
            section.display_order = request.display_order

        if request.title:
            for lang in LANGS:
                val = getattr(request.title, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuQuickSectionTranslation).where(
                        MenuQuickSectionTranslation.section_id == section_id,
                        MenuQuickSectionTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.title = val
                else:
                    db.add(MenuQuickSectionTranslation(section_id=section_id, lang_code=lang, title=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick section updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_quick_section(section_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickSection).where(MenuQuickSection.id == section_id)
        )
        section = result.scalar_one_or_none()
        if not section:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick section not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(section)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick section deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  Quick Section Item
# ─────────────────────────────────────────────────────────────

async def create_quick_section_item(request: CreateQuickSectionItem, db: AsyncSession):
    try:
        section_check = await db.execute(
            select(MenuQuickSection).where(MenuQuickSection.id == request.section_id)
        )
        if not section_check.scalar_one_or_none():
            return JSONResponse(
                content={"status_code": 404, "message": "Quick section not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        item = MenuQuickSectionItem(
            section_id=request.section_id,
            url=request.url,
            display_order=request.display_order,
        )
        db.add(item)
        await db.flush()

        for lang in LANGS:
            db.add(MenuQuickSectionItemTranslation(
                item_id=item.id,
                lang_code=lang,
                label=getattr(request.label, lang),
            ))

        await db.commit()
        await db.refresh(item)
        return JSONResponse(
            content={"status_code": 201, "message": "Quick section item created.", "id": item.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_quick_section_item(item_id: int, request: UpdateQuickSectionItem, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickSectionItem).where(MenuQuickSectionItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick section item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.url is not None:
            item.url = request.url
        if request.display_order is not None:
            item.display_order = request.display_order

        if request.label:
            for lang in LANGS:
                val = getattr(request.label, lang, None)
                if val is None:
                    continue
                tr_result = await db.execute(
                    select(MenuQuickSectionItemTranslation).where(
                        MenuQuickSectionItemTranslation.item_id == item_id,
                        MenuQuickSectionItemTranslation.lang_code == lang,
                    )
                )
                tr = tr_result.scalar_one_or_none()
                if tr:
                    tr.label = val
                else:
                    db.add(MenuQuickSectionItemTranslation(item_id=item_id, lang_code=lang, label=val))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick section item updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_quick_section_item(item_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuQuickSectionItem).where(MenuQuickSectionItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Quick section item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(item)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Quick section item deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
