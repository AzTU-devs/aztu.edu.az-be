import secrets
from datetime import datetime, timezone
from typing import Any

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.research_project import (
    CreateResearchProject,
    UpdateResearchProject,
)
from app.core.logger import get_logger
from app.models.research_project.project import (
    ResearchProject,
    ResearchProjectTr,
    ResearchProjectMember,
)
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload

logger = get_logger(__name__)

_TR_FIELDS = ["name", "project_type", "duration", "leader_name", "budget", "about_html"]


def _project_code_generator() -> str:
    return str(secrets.randbelow(900000) + 100000)


async def _replace_members(project_code: str, members: list[Any] | None, now: datetime, db: AsyncSession):
    """Members are a small ordered roster, so a full replace keeps ordering
    honest and avoids diffing identity-less rows."""
    await db.execute(
        sqlalchemy_delete(ResearchProjectMember).where(
            ResearchProjectMember.project_code == project_code
        )
    )
    for index, member in enumerate(members or []):
        db.add(ResearchProjectMember(
            project_code=project_code,
            full_name=member.full_name,
            display_order=index,
            created_at=now,
            updated_at=now,
        ))


async def _member_names(project_code: str, db: AsyncSession) -> list[str]:
    members_q = await db.execute(
        select(ResearchProjectMember)
        .where(ResearchProjectMember.project_code == project_code)
        .order_by(ResearchProjectMember.display_order.asc(), ResearchProjectMember.id.asc())
    )
    return [member.full_name for member in members_q.scalars().all()]


async def create_research_project(request: CreateResearchProject, db: AsyncSession):
    try:
        project_code = None
        for _ in range(10):
            candidate = _project_code_generator()
            existing_q = await db.execute(
                select(ResearchProject).where(ResearchProject.project_code == candidate)
            )
            if not existing_q.scalar_one_or_none():
                project_code = candidate
                break

        if not project_code:
            return JSONResponse(
                content={"status_code": 500, "message": "Failed to generate unique project code."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        now = datetime.now(timezone.utc)
        project = ResearchProject(
            project_code=project_code,
            image=request.image,
            project_url=request.project_url,
            created_at=now,
            updated_at=now,
        )
        db.add(project)

        for lang_code, translation in [("az", request.az), ("en", request.en)]:
            db.add(ResearchProjectTr(
                project_code=project_code,
                lang_code=lang_code,
                name=translation.name,
                project_type=translation.project_type,
                duration=translation.duration,
                leader_name=translation.leader_name,
                budget=translation.budget,
                about_html=translation.about_html,
                created_at=now,
                updated_at=now,
            ))

        await _replace_members(project_code, request.members, now, db)

        await db.commit()
        await db.refresh(project)

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Research Project created successfully.",
                "data": {
                    "project_code": project.project_code,
                    "created_at": project.created_at.isoformat(),
                },
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_projects(start: int, end: int, lang: str, db: AsyncSession):
    try:
        total_q = await db.execute(select(func.count()).select_from(ResearchProject))
        total = total_q.scalar() or 0

        proj_q = await db.execute(
            select(ResearchProject)
            .order_by(ResearchProject.id.asc())
            .offset(start)
            .limit(end - start)
        )
        projects = proj_q.scalars().all()

        if not projects:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        result = []
        for project in projects:
            tr_q = await db.execute(
                select(ResearchProjectTr).where(
                    ResearchProjectTr.project_code == project.project_code,
                    ResearchProjectTr.lang_code == lang,
                )
            )
            tr = tr_q.scalar_one_or_none()

            # The public page renders whole project cards from this one call,
            # so the summary carries everything a card shows.
            result.append({
                "id": project.id,
                "project_code": project.project_code,
                "image": project.image,
                "project_url": project.project_url,
                "name": tr.name if tr else None,
                "project_type": tr.project_type if tr else None,
                "duration": tr.duration if tr else None,
                "leader_name": tr.leader_name if tr else None,
                "budget": tr.budget if tr else None,
                "about_html": tr.about_html if tr else None,
                "members": await _member_names(project.project_code, db),
                "created_at": project.created_at.isoformat() if project.created_at else None,
            })

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Projects fetched successfully.",
                "projects": result,
                "total": total,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_project(project_code: str, lang_code: str, db: AsyncSession):
    try:
        proj_q = await db.execute(
            select(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        project = proj_q.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Project not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(ResearchProjectTr).where(
                ResearchProjectTr.project_code == project_code,
                ResearchProjectTr.lang_code == lang_code,
            )
        )
        tr = tr_q.scalar_one_or_none()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Project fetched successfully.",
                "project": {
                    "id": project.id,
                    "project_code": project.project_code,
                    "image": project.image,
                    "project_url": project.project_url,
                    "name": tr.name if tr else None,
                    "project_type": tr.project_type if tr else None,
                    "duration": tr.duration if tr else None,
                    "leader_name": tr.leader_name if tr else None,
                    "budget": tr.budget if tr else None,
                    "about_html": tr.about_html if tr else None,
                    "members": await _member_names(project_code, db),
                    "created_at": project.created_at.isoformat() if project.created_at else None,
                    "updated_at": project.updated_at.isoformat() if project.updated_at else None,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_research_project_admin(project_code: str, db: AsyncSession):
    """Both translations at once, shaped for the admin edit form."""
    try:
        proj_q = await db.execute(
            select(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        project = proj_q.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Project not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        tr_q = await db.execute(
            select(ResearchProjectTr).where(ResearchProjectTr.project_code == project_code)
        )
        by_lang = {tr.lang_code: tr for tr in tr_q.scalars().all()}

        def _translation(lang_code: str) -> dict:
            tr = by_lang.get(lang_code)
            return {field: (getattr(tr, field) if tr else None) or "" for field in _TR_FIELDS}

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Project fetched successfully.",
                "project": {
                    "id": project.id,
                    "project_code": project.project_code,
                    "image": project.image,
                    "project_url": project.project_url,
                    "az": _translation("az"),
                    "en": _translation("en"),
                    "members": await _member_names(project_code, db),
                    "created_at": project.created_at.isoformat() if project.created_at else None,
                    "updated_at": project.updated_at.isoformat() if project.updated_at else None,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_research_project(project_code: str, request: UpdateResearchProject, db: AsyncSession):
    try:
        proj_q = await db.execute(
            select(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        project = proj_q.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Project not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data = request.dict(exclude_unset=True)
        now = datetime.now(timezone.utc)

        for field in ["image", "project_url"]:
            if field in data:
                setattr(project, field, data[field])

        for lang_code in ["az", "en"]:
            tr_payload = data.get(lang_code)
            if not tr_payload:
                continue

            tr_q = await db.execute(
                select(ResearchProjectTr).where(
                    ResearchProjectTr.project_code == project_code,
                    ResearchProjectTr.lang_code == lang_code,
                )
            )
            tr = tr_q.scalar_one_or_none()

            if tr:
                for field in _TR_FIELDS:
                    if field in tr_payload:
                        setattr(tr, field, tr_payload[field])
                tr.updated_at = now
            else:
                db.add(ResearchProjectTr(
                    project_code=project_code,
                    lang_code=lang_code,
                    **{field: tr_payload.get(field) for field in _TR_FIELDS},
                    created_at=now,
                    updated_at=now,
                ))

        # `members` is passed as the parsed objects, not the dict slice — the
        # helper reads attributes, and a dict would blow up on `.full_name`.
        if "members" in data:
            await _replace_members(project_code, request.members, now, db)

        project.updated_at = now
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Research Project updated successfully.",
                "data": {
                    "project_code": project.project_code,
                    "updated_at": project.updated_at.isoformat(),
                },
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_research_project(project_code: str, db: AsyncSession):
    try:
        proj_q = await db.execute(
            select(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        project = proj_q.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Project not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_image = project.image
        await db.execute(
            sqlalchemy_delete(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        await db.commit()

        if old_image:
            safe_delete_file(old_image)

        return JSONResponse(
            content={"status_code": 200, "message": "Research Project deleted successfully."},
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def upload_project_image(project_code: str, image: UploadFile, db: AsyncSession):
    try:
        proj_q = await db.execute(
            select(ResearchProject).where(ResearchProject.project_code == project_code)
        )
        project = proj_q.scalar_one_or_none()

        if not project:
            return JSONResponse(
                content={"status_code": 404, "message": "Research Project not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        old_path = project.image
        new_path = await save_upload(image, "research-projects", ALLOWED_IMAGE_MIMES)

        project.image = new_path
        project.updated_at = datetime.now(timezone.utc)
        await db.commit()

        if old_path:
            safe_delete_file(old_path)

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "Project image uploaded successfully.",
                "data": {"image": new_path},
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("500 Internal Server Error")
        await db.rollback()
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
