import os
import random
import traceback

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.models.slider.slider import Slider
from app.models.slider.slider_tr import SliderTranslation
from app.api.v1.schema.slider import ReOrderSlider


def slider_id_generator() -> int:
    return random.randint(100000, 999999)


def _safe_ext(filename: str | None) -> str:
    if not filename or "." not in filename:
        return "jpg"
    ext = filename.rsplit(".", 1)[-1].lower().strip()
    return ext if ext else "jpg"

async def create_slider(request, db: AsyncSession):
    try:
        public_slider_id = slider_id_generator()

        upload_dir = "app/static/sliders"
        os.makedirs(upload_dir, exist_ok=True)

        ext = _safe_ext(getattr(request.image, "filename", None))
        file_path = os.path.join(upload_dir, f"{public_slider_id}.{ext}")

        content = await request.image.read()
        if not content:
            return JSONResponse(
                content={"status_code": 400, "error": "Empty image file"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        with open(file_path, "wb") as f:
            f.write(content)

        image_path = f"static/sliders/{public_slider_id}.{ext}"

        await db.execute(update(Slider).values(display_order=Slider.display_order + 1))
        display_order = 1

        slider = Slider(
            slider_id=public_slider_id,  # ✅ public id stored here
            url=request.url,
            image=image_path,
            display_order=display_order,
            is_active=True,
        )
        db.add(slider)

        await db.flush()  # ✅ now slider.id is available

        db.add(SliderTranslation(slider_id=slider.id, lang_code="az", desc=request.az.desc))
        db.add(SliderTranslation(slider_id=slider.id, lang_code="en", desc=request.en.desc))

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Slider created successfully.",
                "slider_id": slider.slider_id,
                "image": image_path,
                "display_order": display_order,
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        await db.rollback()
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

        return JSONResponse(
            content={
                "status_code": 500,
                "error": repr(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )




async def get_sliders(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Slider))
        total = total_query.scalar() or 0

        slider_query = await db.execute(
            select(Slider)
            .order_by(Slider.display_order.asc())
            .offset(start)
            .limit(end - start)
        )
        sliders = slider_query.scalars().all()

        if not sliders:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        sliders_arr = []
        for s in sliders:
            tr_q = await db.execute(
                select(SliderTranslation).where(
                    SliderTranslation.slider_id == s.slider_id,
                    SliderTranslation.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()

            sliders_arr.append(
                {
                    "id": s.id,
                    "slider_id": s.slider_id,
                    "url": s.url,
                    "image": s.image,
                    "display_order": s.display_order,
                    "desc": tr.desc if tr else None,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                }
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Sliders fetched successfully.",
                "total": total,
                "sliders": sliders_arr,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={"status_code": 500, "error": repr(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def reorder_slider(
    request: ReOrderSlider,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(select(Slider).where(Slider.slider_id == request.slider_id))
        slider_to_move = result.scalar_one_or_none()

        if not slider_to_move:
            return JSONResponse(
                content={"status_code": 404, "error": "Slider not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_order = slider_to_move.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(
                content={"status_code": 200, "message": "No change"},
                status_code=status.HTTP_200_OK,
            )

        if new_order < 1:
            return JSONResponse(
                content={"status_code": 400, "error": "new_order must be >= 1"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if new_order < old_order:
            result = await db.execute(
                select(Slider).where(
                    Slider.display_order >= new_order,
                    Slider.display_order < old_order,
                )
            )
            for s in result.scalars().all():
                s.display_order += 1
                db.add(s)
        else:
            result = await db.execute(
                select(Slider).where(
                    Slider.display_order <= new_order,
                    Slider.display_order > old_order,
                )
            )
            for s in result.scalars().all():
                s.display_order -= 1
                db.add(s)

        slider_to_move.display_order = new_order
        db.add(slider_to_move)

        await db.commit()

        return JSONResponse(
            content={"status_code": 200, "message": "Slider reordered successfully"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": repr(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_slider_by_id(
    slider_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    try:
        slider_q = await db.execute(select(Slider).where(Slider.slider_id == slider_id))
        slider = slider_q.scalar_one_or_none()

        if not slider:
            return JSONResponse(
                content={"status_code": 404, "message": "Slider not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(SliderTranslation).where(
                SliderTranslation.slider_id == slider_id,
                SliderTranslation.lang_code == lang,
            )
        )
        tr = tr_q.scalar_one_or_none()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Slider details fetched successfully.",
                "slider": {
                    "id": slider.id,
                    "slider_id": slider.slider_id,
                    "url": slider.url,
                    "image": slider.image,
                    "display_order": slider.display_order,
                    "desc": tr.desc if tr else None,
                    "created_at": slider.created_at.isoformat() if slider.created_at else None,
                    "updated_at": slider.updated_at.isoformat() if slider.updated_at else None,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={"status_code": 500, "error": repr(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_slider(
    slider_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        slider_q = await db.execute(select(Slider).where(Slider.slider_id == slider_id))
        slider = slider_q.scalar_one_or_none()
        image_rel_path = slider.image if slider else None

        await db.execute(sqlalchemy_delete(SliderTranslation).where(SliderTranslation.slider_id == slider_id))
        result = await db.execute(sqlalchemy_delete(Slider).where(Slider.slider_id == slider_id))

        await db.commit()

        if result.rowcount == 0:
            return JSONResponse(
                content={"status_code": 404, "message": "Slider not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if image_rel_path:
            abs_path = os.path.join("app", image_rel_path)
            if os.path.exists(abs_path):
                try:
                    os.remove(abs_path)
                except Exception:
                    pass

        return JSONResponse(
            content={"status_code": 200, "message": "Slider deleted successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": repr(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

async def update_slider(
    slider_id: int,  
    db: AsyncSession,
    url: str | None = None,
    az_desc: str | None = None,
    en_desc: str | None = None,
    image: UploadFile | None = None,
):
    file_path: str | None = None
    try:
        res = await db.execute(select(Slider).where(Slider.slider_id == slider_id))
        slider = res.scalar_one_or_none()
        if not slider:
            return JSONResponse(
                content={"status_code": 404, "error": "Slider not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if url is not None:
            slider.url = url

        if image is not None:
            upload_dir = "app/static/sliders"
            os.makedirs(upload_dir, exist_ok=True)

            ext = _safe_ext(getattr(image, "filename", None))
            file_path = os.path.join(upload_dir, f"{slider.slider_id}.{ext}")

            content = await image.read()
            if not content:
                return JSONResponse(
                    content={"status_code": 400, "error": "Empty image file"},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            old_abs = os.path.join("app", slider.image) if slider.image else None
            if old_abs and os.path.exists(old_abs) and os.path.abspath(old_abs) != os.path.abspath(file_path):
                try:
                    os.remove(old_abs)
                except Exception:
                    pass

            with open(file_path, "wb") as f:
                f.write(content)

            slider.image = f"static/sliders/{slider.slider_id}.{ext}"

        async def upsert_translation(lang: str, text: str | None):
            if text is None:
                return

            tr_res = await db.execute(
                select(SliderTranslation).where(
                    SliderTranslation.slider_id == slider.id,   
                    SliderTranslation.lang_code == lang,
                )
            )
            tr = tr_res.scalar_one_or_none()
            if tr:
                tr.desc = text
            else:
                db.add(SliderTranslation(slider_id=slider.id, lang_code=lang, desc=text))

        await upsert_translation("az", az_desc)
        await upsert_translation("en", en_desc)

        await db.commit()
        await db.refresh(slider)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Slider updated successfully.",
                "slider": {
                    "id": slider.id,
                    "slider_id": slider.slider_id,
                    "url": slider.url,
                    "image": slider.image,
                    "display_order": slider.display_order,
                    "updated_at": slider.updated_at.isoformat() if slider.updated_at else None,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        await db.rollback()

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

        return JSONResponse(
            content={
                "status_code": 500,
                "error": repr(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )