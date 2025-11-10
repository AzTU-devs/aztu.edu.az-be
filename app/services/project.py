import os
import random
from datetime import datetime
from sqlalchemy import select, func
from app.core.session import get_db
from app.api.v1.schema.project import *
from fastapi import Depends, status, Query
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.models.project.project import Project
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UndefinedTableError
from app.models.project.project_tr import ProjectTranslation

def project_id_generator():
    return random.randint(100000, 999999)

async def create_project(
    request: ProjectCreate = Depends(ProjectCreate.as_form),
    db: AsyncSession = Depends(get_db),
):
    try:
        project_id = project_id_generator()
        upload_dir = "app/static/projects/"
        os.makedirs(upload_dir, exist_ok=True)
        filename = request.bg_image.filename
        ext = filename.split(".")[-1]
        file_path = os.path.join(upload_dir, f"{project_id}.{ext}")
        file_content = await request.bg_image.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        bg_image_path = f"static/projects/{project_id}.{ext}"

        try:
            result = await db.execute(select(Project))
            existing_projects = result.scalars().all()
            for project in existing_projects:
                project.display_order = (project.display_order or 0) + 1
                db.add(project)
            display_order = 1
        except UndefinedTableError:
            display_order = 1

        new_project = Project(
            project_id=project_id,
            bg_image=bg_image_path,
            display_order=display_order,
            is_active=True,
            created_at=datetime.utcnow()
        )

        new_project_az = ProjectTranslation(
            project_id=project_id,
            lang_code="az",
            title=request.az.title,
            desc=request.az.desc,
            html_content=request.az.content_html
        )

        new_project_en = ProjectTranslation(
            project_id=project_id,
            lang_code="en",
            title=request.en.title,
            desc=request.en.desc,
            html_content=request.en.content_html
        )

        db.add(new_project)
        db.add(new_project_az)
        db.add(new_project_en)
        await db.commit()
        await db.refresh(new_project)
        await db.refresh(new_project_az)
        await db.refresh(new_project_en)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Project created successfully."
            }, status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def get_projects(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(4, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total_query = await db.execute(select(func.count()).select_from(Project))
        total = total_query.scalar() or 0

        project_query = await db.execute(
            select(Project)
            .order_by(Project.display_order.asc())
            .offset(start)
            .limit(end - start)
        )

        projects = project_query.scalars().all()

        if not projects:
            return JSONResponse(
                content={
                    "status_code": 204,
                    "message": "No content."
                }, status_code=status.HTTP_204_NO_CONTENT
            )

        projects_arr = []

        for project in projects:
            translation_query = await db.execute(
                select(ProjectTranslation)
                .where(
                    ProjectTranslation.project_id == project.project_id,
                    ProjectTranslation.lang_code == lang
                )
            )

            translation = translation_query.scalar_one_or_none()

            project_obj = {
                "id": project.id,
                "project_id": project.project_id,
                "display_order": project.display_order,
                "title": translation.title,
                "desc": translation.desc,
                "html_content": translation.html_content,
                "created_at": project.created_at.isoformat() if project.created_at else None
            }

            projects_arr.append(project_obj)
        
        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Projects fetched successfully.",
                "total": total,
                "projects": projects_arr
            }, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def reorder_project(
    request: ReOrderProject,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(Project).where(Project.project_id == request.project_id))
        project_to_move = result.scalar_one_or_none()
        if not project_to_move:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "error": "Project not found"
                }, status_code=404
            )

        old_order = project_to_move.display_order
        new_order = request.new_order

        if new_order == old_order:
            return JSONResponse(
                content={
                    "status_code": 200,
                    "message": "No change"
                }, status_code=200)

        if new_order < old_order:
            result = await db.execute(
                select(Project).where(
                    Project.display_order >= new_order,
                    Project.display_order < old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order += 1
                db.add(p)
        else:
            result = await db.execute(
                select(Project).where(
                    Project.display_order <= new_order,
                    Project.display_order > old_order
                )
            )
            projects_to_shift = result.scalars().all()
            for p in projects_to_shift:
                p.display_order -= 1
                db.add(p)

        project_to_move.display_order = new_order
        db.add(project_to_move)

        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project reordered successfully"
            }, status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=500
        )

async def get_project_by_id(
    project_id: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        project_query = await db.execute(
            select(Project)
            .where(Project.project_id == project_id)
        )

        project = project_query.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Project not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        translation_query = await db.execute(
            select(ProjectTranslation)
            .where(
                ProjectTranslation.project_id == project_id,
                ProjectTranslation.lang_code == lang
            )
        )

        translation = translation_query.scalar_one_or_none()

        project_obj = {
            "id": project.id,
            "bg_image": project.bg_image,
            "title": translation.title,
            "desc": translation.desc,
            "html_content": translation.html_content,
            "display_order": project.display_order,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project details fetched successfully.",
                "project": project_obj
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=500
        )

from sqlalchemy import delete as sqlalchemy_delete

async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        translations_stmt = sqlalchemy_delete(ProjectTranslation).where(
            ProjectTranslation.project_id == project_id
        )
        await db.execute(translations_stmt)

        project_stmt = sqlalchemy_delete(Project).where(Project.project_id == project_id)
        result = await db.execute(project_stmt)
        await db.commit()

        if result.rowcount == 0:
            return JSONResponse(
                content={
                    "status_code": 404,
                    "message": "Project not found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project deleted successfully."
            }, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "error": str(e)
            }, status_code=500
        )