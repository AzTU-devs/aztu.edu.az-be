from typing import Any, Dict, List, Optional

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

            # Auto-generate direct_url if it's a leaf
            header_url = header.direct_url
            if not header.has_subitems and not header_url:
                header_url = f"/{lang_code}/{tr.slug}"

            items_arr = []
            if header.has_subitems:
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

                    # Auto-generate item url: /{lang}/{header_slug}/{item_slug}
                    item_url = item.direct_url
                    if not item.has_subitems and not item_url:
                        item_url = f"/{lang_code}/{tr.slug}/{item_tr.slug}"

                    sub_items_arr = []
                    if item.has_subitems:
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

                            # Auto-generate sub-item url: /{lang}/{header_slug}/{item_slug}/{sub_item_slug}
                            sub_url = sub.direct_url
                            if not sub_url:
                                sub_url = f"/{lang_code}/{tr.slug}/{item_tr.slug}/{sub_tr.slug}"

                            sub_items_arr.append({
                                "id": sub.id,
                                "title": sub_tr.title,
                                "slug": sub_tr.slug,
                                "direct_url": sub_url,
                            })

                    items_arr.append({
                        "id": item.id,
                        "title": item_tr.title,
                        "slug": item_tr.slug,
                        "direct_url": item_url,
                        "sub_items": sub_items_arr,
                    })

            data.append({
                "id": header.id,
                "image_url": header.image_url,
                "title": tr.title,
                "slug": tr.slug,
                "direct_url": header_url,
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
# GET  —  admin
# ─────────────────────────────────────────────────────────────

def _by_parent_and_lang(rows, parent_attr: str) -> Dict[int, Dict[str, Any]]:
    """{parent_id: {"az": translation, "en": translation}}."""
    grouped: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        grouped.setdefault(getattr(row, parent_attr), {})[row.lang_code] = row
    return grouped


def _titles(by_lang: Dict[str, Any]) -> Dict[str, str]:
    """Both translations side by side, plus an az-preferred pair the editor lists
    rows by. A row half-translated still renders rather than vanishing."""
    az = by_lang.get("az")
    en = by_lang.get("en")
    primary = az or en
    return {
        "title": primary.title if primary else "",
        "slug": primary.slug if primary else "",
        "title_az": az.title if az else "",
        "title_en": en.title if en else "",
        "slug_az": az.slug if az else "",
        "slug_en": en.slug if en else "",
    }


async def get_header_menu_admin(db: AsyncSession):
    """The whole tree as the dashboard editor needs it.

    Three things the public reader deliberately withholds and the editor cannot
    work without: inactive rows (otherwise deactivating one hides it forever),
    both translations at once, and the raw `display_order` / `has_subitems` /
    `is_active` columns it has to round-trip on save.

    The header menu is a handful of rows by nature, so each level loads in one
    query and is stitched in memory rather than walked per-parent.
    """
    try:
        headers = (await db.execute(
            select(MenuHeader).order_by(
                MenuHeader.display_order.asc(), MenuHeader.id.asc()
            )
        )).scalars().all()

        items = (await db.execute(
            select(MenuHeaderItem).order_by(
                MenuHeaderItem.display_order.asc(), MenuHeaderItem.id.asc()
            )
        )).scalars().all()

        sub_items = (await db.execute(
            select(MenuHeaderSubItem).order_by(
                MenuHeaderSubItem.display_order.asc(), MenuHeaderSubItem.id.asc()
            )
        )).scalars().all()

        header_tr = _by_parent_and_lang(
            (await db.execute(select(MenuHeaderTranslation))).scalars().all(),
            "header_id",
        )
        item_tr = _by_parent_and_lang(
            (await db.execute(select(MenuHeaderItemTranslation))).scalars().all(),
            "item_id",
        )
        sub_tr = _by_parent_and_lang(
            (await db.execute(select(MenuHeaderSubItemTranslation))).scalars().all(),
            "sub_item_id",
        )

        subs_by_item: Dict[int, List[dict]] = {}
        for sub in sub_items:
            subs_by_item.setdefault(sub.item_id, []).append({
                "id": sub.id,
                "item_id": sub.item_id,
                "direct_url": sub.direct_url,
                "display_order": sub.display_order,
                "is_active": sub.is_active,
                **_titles(sub_tr.get(sub.id, {})),
            })

        items_by_header: Dict[int, List[dict]] = {}
        for item in items:
            items_by_header.setdefault(item.header_id, []).append({
                "id": item.id,
                "header_id": item.header_id,
                "direct_url": item.direct_url,
                "has_subitems": item.has_subitems,
                "display_order": item.display_order,
                "is_active": item.is_active,
                "sub_items": subs_by_item.get(item.id, []),
                **_titles(item_tr.get(item.id, {})),
            })

        data = [
            {
                "id": header.id,
                "image_url": header.image_url,
                "direct_url": header.direct_url,
                "has_subitems": header.has_subitems,
                "display_order": header.display_order,
                "is_active": header.is_active,
                "items": items_by_header.get(header.id, []),
                **_titles(header_tr.get(header.id, {})),
            }
            for header in headers
        ]

        return JSONResponse(
            content={"status_code": 200, "data": data},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        logger.exception("get_header_menu_admin failed")
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
    has_subitems: bool,
    display_order: int,
    title_az: str,
    title_en: str,
    db: AsyncSession,
):
    try:
        header = MenuHeader(
            image_url=image_url,
            direct_url=direct_url or None,
            has_subitems=has_subitems,
            display_order=display_order,
        )
        db.add(header)
        await db.flush()

        for lang, title in [("az", title_az), ("en", title_en)]:
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
    has_subitems: Optional[bool],
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

        if has_subitems is not None:
            header.has_subitems = has_subitems

        if direct_url is not None:
            header.direct_url = direct_url if direct_url != "" else None

        lang_data = {"az": title_az, "en": title_en}
        for lang, t_val in lang_data.items():
            if t_val is None:
                continue
            tr_result = await db.execute(
                select(MenuHeaderTranslation).where(
                    MenuHeaderTranslation.header_id == header_id,
                    MenuHeaderTranslation.lang_code == lang,
                )
            )
            tr = tr_result.scalar_one_or_none()
            if tr:
                tr.title = t_val
                tr.slug = make_slug(t_val)
            else:
                db.add(MenuHeaderTranslation(
                    header_id=header_id,
                    lang_code=lang,
                    title=t_val,
                    slug=make_slug(t_val),
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
        if not parent.has_subitems:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "message": "Cannot add items to a header that is marked as leaf.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        item = MenuHeaderItem(
            header_id=request.header_id,
            direct_url=request.direct_url or None,
            has_subitems=request.has_subitems,
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
        if request.has_subitems is not None:
            item.has_subitems = request.has_subitems
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
        if not parent.has_subitems:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "message": "Cannot add sub-items to an item that is marked as leaf.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        sub = MenuHeaderSubItem(
            item_id=request.item_id,
            direct_url=request.direct_url or None,
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
            sub.direct_url = request.direct_url if request.direct_url != "" else None

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
