from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.api.v1.schema.cafedra import CreateCafedra, UpdateCafedra, LaboratoryItem
from app.services.cafedra import (
    create_cafedra,
    delete_cafedra,
    get_cafedra,
    get_cafedras,
    update_cafedra,
    upload_cafedra_director_image,
    upload_cafedra_deputy_director_image,
    upload_cafedra_worker_image,
    create_laboratory,
    get_all_laboratories,
    get_cafedra_laboratories,
    upload_laboratory_image,
)

router = APIRouter()


@router.get("/admin/all")
async def get_cafedras_endpoint_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/public/all")
async def get_cafedras_endpoint_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/laboratories/all")
async def get_all_laboratories_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_laboratories(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/{cafedra_code}")
async def get_cafedra_details_endpoint(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra(
        cafedra_code=cafedra_code,
        lang_code=lang_code,
        db=db,
    )


@router.get("/{cafedra_code}/laboratories")
async def get_cafedra_laboratories_endpoint(
    cafedra_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra_laboratories(
        cafedra_code=cafedra_code,
        lang=lang,
        db=db,
    )


@router.post("/create")
async def create_cafedra_endpoint(
    request: CreateCafedra,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await create_cafedra(
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/laboratories")
async def create_laboratory_endpoint(
    cafedra_code: str,
    request: LaboratoryItem,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await create_laboratory(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.put("/{cafedra_code}")
async def update_cafedra_endpoint(
    cafedra_code: str,
    request: UpdateCafedra,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await update_cafedra(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.delete("/{cafedra_code}")
async def delete_cafedra_endpoint(
    cafedra_code: str,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await delete_cafedra(
        cafedra_code=cafedra_code,
        db=db,
    )


@router.put("/{cafedra_code}/director/image")
async def upload_cafedra_director_image_endpoint(
    cafedra_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_director_image(
        cafedra_code=cafedra_code,
        image=image,
        db=db,
    )


@router.put("/deputy-directors/{deputy_director_id}/image")
async def upload_cafedra_deputy_director_image_endpoint(
    deputy_director_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_deputy_director_image(
        deputy_director_id=deputy_director_id,
        image=image,
        db=db,
    )


@router.put("/workers/{worker_id}/image")
async def upload_cafedra_worker_image_endpoint(
    worker_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_worker_image(
        worker_id=worker_id,
        image=image,
        db=db,
    )


@router.put("/laboratories/{laboratory_id}/image")
async def upload_laboratory_image_endpoint(
    laboratory_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await upload_laboratory_image(
        laboratory_id=laboratory_id,
        image=image,
        db=db,
    )
