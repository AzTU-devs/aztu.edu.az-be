from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.employee import (
    create_employee,
    get_employees,
    get_employee,
    update_employee,
    delete_employee,
)
from app.api.v1.schema.employee import CreateEmployee, UpdateEmployee

router = APIRouter()


@router.get("/admin/all")
async def get_employees_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: Optional[str] = Query(None, description="Filter by faculty code"),
    cafedra_code: Optional[str] = Query(None, description="Filter by cafedra code"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await get_employees(
        start=start,
        end=end,
        lang=lang,
        db=db,
        faculty_code=faculty_code,
        cafedra_code=cafedra_code,
    )


@router.get("/public/all")
async def get_employees_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: Optional[str] = Query(None, description="Filter by faculty code"),
    cafedra_code: Optional[str] = Query(None, description="Filter by cafedra code"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_employees(
        start=start,
        end=end,
        lang=lang,
        db=db,
        faculty_code=faculty_code,
        cafedra_code=cafedra_code,
    )


@router.get("/{employee_code}")
async def get_employee_detail(
    employee_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_employee(
        employee_code=employee_code,
        lang_code=lang_code,
        db=db,
    )


@router.post("/create")
async def create_employee_endpoint(
    request: CreateEmployee = Depends(CreateEmployee.as_form),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await create_employee(
        request=request,
        db=db,
    )


@router.put("/{employee_code}")
async def update_employee_endpoint(
    employee_code: str,
    request: UpdateEmployee = Depends(UpdateEmployee.as_form),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await update_employee(
        employee_code=employee_code,
        request=request,
        db=db,
    )


@router.delete("/{employee_code}")
async def delete_employee_endpoint(
    employee_code: str,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    return await delete_employee(
        employee_code=employee_code,
        db=db,
    )
