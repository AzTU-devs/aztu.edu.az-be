from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.faculty import (
    create_faculty,
    get_faculties,
    get_faculty,
    update_faculty,
    delete_faculty,
    upload_director_profile_image,
    upload_deputy_dean_profile_image,
    upload_worker_profile_image,
    get_directions_of_action,
    create_direction_of_action,
    update_direction_of_action,
    delete_direction_of_action,
    create_worker,
)
from app.api.v1.schema.faculty import CreateFaculty, UpdateFaculty, CreateDirectionOfAction, UpdateDirectionOfAction, Worker

router = APIRouter()


@router.get("/admin/all")
async def get_faculties_endpoint_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_faculties(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/public/all")
async def get_faculties_endpoint_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_faculties(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/{faculty_code}")
async def get_faculty_details_endpoint(
    faculty_code: str,
    lang_code: str | None = Query(None, description="Language code (az or en). If omitted, returns bilingual data."),
    db: AsyncSession = Depends(get_db),
):
    return await get_faculty(
        faculty_code=faculty_code,
        lang_code=lang_code,
        db=db,
    )


@router.patch("/{faculty_code}")
async def patch_faculty_endpoint(
    faculty_code: str,
    request: UpdateFaculty,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_faculty(
        faculty_code=faculty_code,
        request=request,
        db=db,
    )


@router.post("/create")
async def create_faculty_endpoint(
    request: CreateFaculty,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_faculty(
        request=request,
        db=db,
    )


@router.delete("/{faculty_code}")
async def delete_faculty_endpoint(
    faculty_code: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_faculty(
        faculty_code=faculty_code,
        db=db,
    )


@router.put("/{faculty_code}/director/image")
async def upload_director_image_endpoint(
    faculty_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_director_profile_image(
        faculty_code=faculty_code,
        image=image,
        db=db,
    )


@router.put("/deputy-deans/{deputy_dean_id}/image")
async def upload_deputy_dean_image_endpoint(
    deputy_dean_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_deputy_dean_profile_image(
        deputy_dean_id=deputy_dean_id,
        image=image,
        db=db,
    )


@router.put("/workers/{worker_id}/image")
async def upload_worker_image_endpoint(
    worker_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_worker_profile_image(
        worker_id=worker_id,
        image=image,
        db=db,
    )


@router.post("/{faculty_code}/workers")
async def create_worker_endpoint(
    faculty_code: str,
    request: Worker,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_worker(
        faculty_code=faculty_code,
        request=request,
        db=db,
    )


@router.get("/{faculty_code}/directions-of-action")
async def get_directions_of_action_endpoint(
    faculty_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_directions_of_action(
        faculty_code=faculty_code,
        lang_code=lang,
        db=db,
    )


@router.post("/{faculty_code}/directions-of-action")
async def create_direction_of_action_endpoint(
    faculty_code: str,
    request: CreateDirectionOfAction,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_direction_of_action(
        faculty_code=faculty_code,
        request=request,
        db=db,
    )


@router.put("/{faculty_code}/directions-of-action/{direction_id}")
async def update_direction_of_action_endpoint(
    faculty_code: str,
    direction_id: int,
    request: UpdateDirectionOfAction,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_direction_of_action(
        direction_id=direction_id,
        request=request,
        db=db,
    )


@router.delete("/{faculty_code}/directions-of-action/{direction_id}")
async def delete_direction_of_action_endpoint(
    faculty_code: str,
    direction_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_direction_of_action(
        direction_id=direction_id,
        db=db,
    )
