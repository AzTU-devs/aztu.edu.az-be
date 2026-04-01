from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.menu.header import (
    MenuHeader, MenuHeaderTranslation,
    MenuHeaderItem, MenuHeaderItemTranslation,
    MenuHeaderSubItem, MenuHeaderSubItemTranslation,
)
from app.api.v1.schema.menu import (
    CreateHeaderItem, UpdateHeaderItem,
    CreateHeaderSubItem, UpdateHeaderSubItem,
)
from app.utils.file_upload import safe_delete_file
from app.utils.slug import make_slug

logger = get_logger(__name__)

LANGS = ("az", "en")


# ─────────────────────────────────────────────────────────────
# GET  —  public
# ─────────────────────────────────────────────────────────────

async def get_header_menu(lang_code: str, db: AsyncSession):
    try:
        headers_result = await db.execute(
            select(MenuHeader)
            .where(MenuHeader.is_active == True)
            .order_by(MenuHeader.display_order.asc())
        )
        headers = headers_result.scalars().all()

        data = []
        for header in headers:
            tr_result = await db.execute(
                select(MenuHeaderTranslation).where(
                    MenuHeaderTranslation.header_id == header.id,
                    MenuHeaderTranslation.lang_code == lang_code,
                )
            )
            tr = tr_result.scalar_one_or_none()
            if not tr:
                continue

            items_arr = []
            if not header.direct_url:
                items_result = await db.execute(
                    select(MenuHeaderItem)
                    .where(
                        MenuHeaderItem.header_id == header.id,
                        MenuHeaderItem.is_active == True,
                    )
                    .order_by(MenuHeaderItem.display_order.asc())
                )
                for item in items_result.scalars().all():
                    item_tr_result = await db.execute(
                        select(MenuHeaderItemTranslation).where(
                            MenuHeaderItemTranslation.item_id == item.id,
                            MenuHeaderItemTranslation.lang_code == lang_code,
                        )
                    )
                    item_tr = item_tr_result.scalar_one_or_none()
                    if not item_tr:
                        continue

                    sub_items_arr = []
                    if not item.direct_url:
                        sub_result = await db.execute(
                            select(MenuHeaderSubItem)
                            .where(
                                MenuHeaderSubItem.item_id == item.id,
                                MenuHeaderSubItem.is_active == True,
                            )
                            .order_by(MenuHeaderSubItem.display_order.asc())
                        )
                        for sub in sub_result.scalars().all():
                            sub_tr_result = await db.execute(
                                select(MenuHeaderSubItemTranslation).where(
                                    MenuHeaderSubItemTranslation.sub_item_id == sub.id,
                                    MenuHeaderSubItemTranslation.lang_code == lang_code,
                                )
                            )
                            sub_tr = sub_tr_result.scalar_one_or_none()
                            if not sub_tr:
                                continue
                            sub_items_arr.append({
                                "id": sub.id,
                                "title": sub_tr.title,
                                "slug": sub_tr.slug,
                                "direct_url": sub.direct_url,
                            })

                    items_arr.append({
                        "id": item.id,
                        "title": item_tr.title,
                        "slug": item_tr.slug,
                        "direct_url": item.direct_url,
                        "sub_items": sub_items_arr,
                    })

            data.append({
                "id": header.id,
                "image_url": header.image_url,
                "title": tr.title,
                "slug": tr.slug,
                "direct_url": header.direct_url,
                "items": items_arr,
            })

        return JSONResponse(
            content={"status_code": 200, "data": data},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("get_header_menu failed")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeader (main title)
# ─────────────────────────────────────────────────────────────

async def create_header(
    image_url: Optional[str],
    direct_url: Optional[str],
    display_order: int,
    title_az: str,
    title_en: str,
    db: AsyncSession,
):
    try:
        header = MenuHeader(
            image_url=image_url,
            direct_url=direct_url or None,
            display_order=display_order,
        )
        db.add(header)
        await db.flush()

        for lang, title in (("az", title_az), ("en", title_en)):
            db.add(MenuHeaderTranslation(
                header_id=header.id,
                lang_code=lang,
                title=title,
                slug=make_slug(title),
            ))

        await db.commit()
        await db.refresh(header)
        return JSONResponse(
            content={"status_code": 201, "message": "Header created.", "id": header.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        logger.exception("create_header failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_header(
    header_id: int,
    image_url: Optional[str],
    direct_url: Optional[str],
    display_order: Optional[int],
    is_active: Optional[bool],
    title_az: Optional[str],
    title_en: Optional[str],
    db: AsyncSession,
):
    try:
        result = await db.execute(
            select(MenuHeader).where(MenuHeader.id == header_id)
        )
        header = result.scalar_one_or_none()
        if not header:
            return JSONResponse(
                content={"status_code": 404, "message": "Header not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if image_url is not None:
            if header.image_url:
                old_rel = header.image_url.replace("https://aztu.edu.az/", "", 1)
                safe_delete_file(old_rel)
            header.image_url = image_url

        if display_order is not None:
            header.display_order = display_order

        if is_active is not None:
            header.is_active = is_active

        # "" clears the field; non-empty string sets it; None = no change
        if direct_url is not None:
            header.direct_url = direct_url if direct_url != "" else None

        title_map = {"az": title_az, "en": title_en}
        for lang, title_val in title_map.items():
            if title_val is None:
                continue
            tr_result = await db.execute(
                select(MenuHeaderTranslation).where(
                    MenuHeaderTranslation.header_id == header_id,
                    MenuHeaderTranslation.lang_code == lang,
                )
            )
            tr = tr_result.scalar_one_or_none()
            if tr:
                tr.title = title_val
                tr.slug = make_slug(title_val)
            else:
                db.add(MenuHeaderTranslation(
                    header_id=header_id,
                    lang_code=lang,
                    title=title_val,
                    slug=make_slug(title_val),
                ))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("update_header failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_header(header_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuHeader).where(MenuHeader.id == header_id)
        )
        header = result.scalar_one_or_none()
        if not header:
            return JSONResponse(
                content={"status_code": 404, "message": "Header not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if header.image_url:
            old_rel = header.image_url.replace("https://aztu.edu.az/", "", 1)
            safe_delete_file(old_rel)
        await db.delete(header)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("delete_header failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeaderItem (first-level dropdown)
# ─────────────────────────────────────────────────────────────

async def create_header_item(request: CreateHeaderItem, db: AsyncSession):
    try:
        parent_result = await db.execute(
            select(MenuHeader).where(MenuHeader.id == request.header_id)
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            return JSONResponse(
                content={"status_code": 404, "message": "Header not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if parent.direct_url:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "message": "Cannot add items to a header that already has a direct URL.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        item = MenuHeaderItem(
            header_id=request.header_id,
            direct_url=request.direct_url or None,
            display_order=request.display_order,
        )
        db.add(item)
        await db.flush()

        for lang, title in (("az", request.title_az), ("en", request.title_en)):
            db.add(MenuHeaderItemTranslation(
                item_id=item.id,
                lang_code=lang,
                title=title,
                slug=make_slug(title),
            ))

        await db.commit()
        await db.refresh(item)
        return JSONResponse(
            content={"status_code": 201, "message": "Header item created.", "id": item.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        logger.exception("create_header_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_header_item(item_id: int, request: UpdateHeaderItem, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuHeaderItem).where(MenuHeaderItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.display_order is not None:
            item.display_order = request.display_order
        if request.is_active is not None:
            item.is_active = request.is_active
        if request.direct_url is not None:
            item.direct_url = request.direct_url if request.direct_url != "" else None

        title_map = {"az": request.title_az, "en": request.title_en}
        for lang, title_val in title_map.items():
            if title_val is None:
                continue
            tr_result = await db.execute(
                select(MenuHeaderItemTranslation).where(
                    MenuHeaderItemTranslation.item_id == item_id,
                    MenuHeaderItemTranslation.lang_code == lang,
                )
            )
            tr = tr_result.scalar_one_or_none()
            if tr:
                tr.title = title_val
                tr.slug = make_slug(title_val)
            else:
                db.add(MenuHeaderItemTranslation(
                    item_id=item_id,
                    lang_code=lang,
                    title=title_val,
                    slug=make_slug(title_val),
                ))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header item updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("update_header_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_header_item(item_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuHeaderItem).where(MenuHeaderItem.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return JSONResponse(
                content={"status_code": 404, "message": "Item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(item)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header item deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("delete_header_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeaderSubItem (second-level leaf)
# ─────────────────────────────────────────────────────────────

async def create_header_sub_item(request: CreateHeaderSubItem, db: AsyncSession):
    try:
        parent_result = await db.execute(
            select(MenuHeaderItem).where(MenuHeaderItem.id == request.item_id)
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            return JSONResponse(
                content={"status_code": 404, "message": "Item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if parent.direct_url:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "message": "Cannot add sub-items to an item that already has a direct URL.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        sub = MenuHeaderSubItem(
            item_id=request.item_id,
            direct_url=request.direct_url,
            display_order=request.display_order,
        )
        db.add(sub)
        await db.flush()

        for lang, title in (("az", request.title_az), ("en", request.title_en)):
            db.add(MenuHeaderSubItemTranslation(
                sub_item_id=sub.id,
                lang_code=lang,
                title=title,
                slug=make_slug(title),
            ))

        await db.commit()
        await db.refresh(sub)
        return JSONResponse(
            content={"status_code": 201, "message": "Header sub-item created.", "id": sub.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        logger.exception("create_header_sub_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_header_sub_item(
    sub_item_id: int, request: UpdateHeaderSubItem, db: AsyncSession
):
    try:
        result = await db.execute(
            select(MenuHeaderSubItem).where(MenuHeaderSubItem.id == sub_item_id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            return JSONResponse(
                content={"status_code": 404, "message": "Sub-item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if request.display_order is not None:
            sub.display_order = request.display_order
        if request.is_active is not None:
            sub.is_active = request.is_active
        if request.direct_url is not None:
            sub.direct_url = request.direct_url

        title_map = {"az": request.title_az, "en": request.title_en}
        for lang, title_val in title_map.items():
            if title_val is None:
                continue
            tr_result = await db.execute(
                select(MenuHeaderSubItemTranslation).where(
                    MenuHeaderSubItemTranslation.sub_item_id == sub_item_id,
                    MenuHeaderSubItemTranslation.lang_code == lang,
                )
            )
            tr = tr_result.scalar_one_or_none()
            if tr:
                tr.title = title_val
                tr.slug = make_slug(title_val)
            else:
                db.add(MenuHeaderSubItemTranslation(
                    sub_item_id=sub_item_id,
                    lang_code=lang,
                    title=title_val,
                    slug=make_slug(title_val),
                ))

        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header sub-item updated."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("update_header_sub_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_header_sub_item(sub_item_id: int, db: AsyncSession):
    try:
        result = await db.execute(
            select(MenuHeaderSubItem).where(MenuHeaderSubItem.id == sub_item_id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            return JSONResponse(
                content={"status_code": 404, "message": "Sub-item not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await db.delete(sub)
        await db.commit()
        return JSONResponse(
            content={"status_code": 200, "message": "Header sub-item deleted."},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("delete_header_sub_item failed")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
