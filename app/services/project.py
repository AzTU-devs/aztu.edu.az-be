import secrets
from datetime import datetime, timezone
from sqlalchemy import select, func, delete as sqlalchemy_delete
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)
from app.api.v1.schema.project import *
from fastapi import Depends, status, Query
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES
from app.utils.html_sanitizer import sanitize_html
from app.models.project.project import Project
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.project.project_tr import ProjectTranslation


def project_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


async def create_project(
    request: ProjectCreate = Depends(ProjectCreate.as_form),
    db: AsyncSession = Depends(get_db),
):
    saved_files: list[str] = []
    try:
        project_id = project_id_generator()

        bg_image_path = await save_upload(request.bg_image, "projects", ALLOWED_IMAGE_MIMES)
        saved_files.append(bg_image_path)

        try:
            for p in (await db.execute(select(Project))).scalars().all():
                p.display_order = (p.display_order or 0) + 1
                db.add(p)
            display_order = 1
        except UndefinedTableError:
            display_order = 1

        db.add(Project(
            project_id=project_id,
            bg_image=bg_image_path,
            display_order=display_order,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        ))
        db.add(ProjectTranslation(
            project_id=project_id, lang_code="az",
            title=request.az.title,
            description=request.az.description,
            html_content=sanitize_html(request.az.content_html)
        ))
        db.add(ProjectTranslation(
            project_id=project_id, lang_code="en",
            title=request.en.title,
            description=request.en.description,
            html_content=sanitize_html(request.en.content_html)
        ))
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Project created successfully."},
            status_code=status.HTTP_201_CREATED
        )

    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create project")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_projects(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, le=100, description="End index (max 100)"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(Project))).scalar() or 0
        projects = (await db.execute(
            select(Project).order_by(Project.display_order.asc()).offset(start).limit(end - start)
        )).scalars().all()

        if not projects:
            return JSONResponse(content={"status_code": 204, "message": "No content."}, status_code=status.HTTP_204_NO_CONTENT)

        projects_arr = []
        for project in projects:
            tr = (await db.execute(
                select(ProjectTranslation).where(
                    ProjectTranslation.project_id == project.project_id,
                    ProjectTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            projects_arr.append({
                "id": project.id,
                "project_id": project.project_id,
                "display_order": project.display_order,
                "title": tr.title if tr else None,
                "description": tr.description if tr else None,
                "html_content": tr.html_content if tr else None,
                "created_at": project.created_at.isoformat() if project.created_at else None,
            })

        return JSONResponse(
            content={"status_code": 200, "message": "Projects fetched successfully.", "total": total, "projects": projects_arr}
        )

    except Exception:
        logger.exception("Failed to fetch projects")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def reorder_project(
    request: ReOrderProject,
    db: AsyncSession = Depends(get_db)
):
    try:
        p = (await db.execute(select(Project).where(Project.project_id == request.project_id))).scalar_one_or_none()
        if not p:
            return JSONResponse(content={"status_code": 404, "error": "Project not found"}, status_code=404)

        old_order = p.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(content={"status_code": 200, "message": "No change"})

        if new_order < old_order:
            rows = (await db.execute(select(Project).where(Project.display_order >= new_order, Project.display_order < old_order))).scalars().all()
            for r in rows:
                r.display_order += 1
                db.add(r)
        else:
            rows = (await db.execute(select(Project).where(Project.display_order <= new_order, Project.display_order > old_order))).scalars().all()
            for r in rows:
                r.display_order -= 1
                db.add(r)

        p.display_order = new_order
        db.add(p)
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Project reordered successfully"})

    except Exception:
        logger.exception("Failed to reorder project")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)


async def get_project_by_id(
    project_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        project = (await db.execute(select(Project).where(Project.project_id == project_id))).scalar_one_or_none()
        if not project:
            return JSONResponse(content={"status_code": 404, "message": "Project not found."}, status_code=status.HTTP_404_NOT_FOUND)

        tr = (await db.execute(
            select(ProjectTranslation).where(ProjectTranslation.project_id == project_id, ProjectTranslation.lang_code == lang)
        )).scalar_one_or_none()

        return JSONResponse(content={
            "status_code": 200,
            "message": "Project details fetched successfully.",
            "project": {
                "id": project.id,
                "bg_image": project.bg_image,
                "title": tr.title if tr else None,
                "description": tr.description if tr else None,
                "html_content": tr.html_content if tr else None,
                "display_order": project.display_order,
                "created_at": project.created_at.isoformat() if project.created_at else None,
                "updated_at": project.updated_at.isoformat() if project.updated_at else None,
            }
        })

    except Exception:
        logger.exception("Failed to fetch project by id")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)


async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Fetch project first to get the bg_image path
        project = (await db.execute(select(Project).where(Project.project_id == project_id))).scalar_one_or_none()
        if not project:
            return JSONResponse(content={"status_code": 404, "message": "Project not found."}, status_code=status.HTTP_404_NOT_FOUND)

        bg_image_path = project.bg_image

        await db.execute(sqlalchemy_delete(ProjectTranslation).where(ProjectTranslation.project_id == project_id))
        await db.execute(sqlalchemy_delete(Project).where(Project.project_id == project_id))
        await db.commit()

        safe_delete_file(bg_image_path)

        return JSONResponse(content={"status_code": 200, "message": "Project deleted successfully."})

    except Exception:
        logger.exception("Failed to delete project")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)
