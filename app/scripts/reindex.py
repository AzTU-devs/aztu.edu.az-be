"""Rebuild Elasticsearch indices from PostgreSQL.

Usage:
    python -m app.scripts.reindex                  # rebuild all types
    python -m app.scripts.reindex --type news      # one type only
    python -m app.scripts.reindex --type news --limit 100
"""

from __future__ import annotations

import argparse
import asyncio
import logging

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.elasticsearch import get_es, close_es
from app.services.search import (
    DOC_TYPES,
    ensure_indices,
    reindex_news,
    reindex_announcement,
    reindex_project,
    reindex_collaboration,
    reindex_faculty,
    reindex_cafedra,
    reindex_department,
    reindex_employee,
    reindex_research_institute,
)
from app.services.search.service import drop_indices

logger = logging.getLogger("aztu.reindex")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


async def _ids_for(doc_type: str, db) -> list:
    """Return the list of primary identifiers for a given doc type."""
    if doc_type == "news":
        from app.models.news.news import News
        rows = (await db.execute(select(News.news_id))).scalars().all()
        return list(rows)
    if doc_type == "announcement":
        from app.models.announcement.announcement import Announcement
        rows = (await db.execute(select(Announcement.announcement_id))).scalars().all()
        return list(rows)
    if doc_type == "project":
        from app.models.project.project import Project
        rows = (await db.execute(select(Project.project_id))).scalars().all()
        return list(rows)
    if doc_type == "collaboration":
        from app.models.collaboration.collaboration import Collaboration
        rows = (await db.execute(select(Collaboration.collaboration_id))).scalars().all()
        return list(rows)
    if doc_type == "faculty":
        from app.models.faculties.faculties import Faculty
        rows = (await db.execute(select(Faculty.faculty_code))).scalars().all()
        return list(rows)
    if doc_type == "cafedra":
        from app.models.cafedras.cafedras import Cafedra
        rows = (await db.execute(select(Cafedra.cafedra_code))).scalars().all()
        return list(rows)
    if doc_type == "department":
        from app.models.departments.department import Department
        rows = (await db.execute(select(Department.department_code))).scalars().all()
        return list(rows)
    if doc_type == "employee":
        from app.models.employee.employee import Employee
        rows = (await db.execute(select(Employee.employee_code))).scalars().all()
        return list(rows)
    if doc_type == "research_institute":
        from app.models.research_institute.institute import ResearchInstitute
        rows = (await db.execute(select(ResearchInstitute.institute_code))).scalars().all()
        return list(rows)
    return []


REINDEX_FN = {
    "news": reindex_news,
    "announcement": reindex_announcement,
    "project": reindex_project,
    "collaboration": reindex_collaboration,
    "faculty": reindex_faculty,
    "cafedra": reindex_cafedra,
    "department": reindex_department,
    "employee": reindex_employee,
    "research_institute": reindex_research_institute,
}


async def reindex_type(es, db, doc_type: str, limit: int | None = None) -> int:
    fn = REINDEX_FN[doc_type]
    ids = await _ids_for(doc_type, db)
    if limit:
        ids = ids[:limit]
    logger.info("Reindexing %s: %d rows", doc_type, len(ids))
    for ident in ids:
        await fn(es, db, ident)
    return len(ids)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", dest="doc_type", choices=list(DOC_TYPES),
                        help="Reindex only one type (default: all)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Cap rows per type (debug)")
    parser.add_argument("--no-drop", action="store_true",
                        help="Skip deleting existing indices before rebuild")
    args = parser.parse_args()

    types = (args.doc_type,) if args.doc_type else DOC_TYPES

    es = await get_es()
    try:
        if not args.no_drop:
            logger.info("Dropping indices for: %s", ", ".join(types))
            await drop_indices(es, doc_types=types)
        await ensure_indices(es)

        async with AsyncSessionLocal() as db:
            total = 0
            for doc_type in types:
                total += await reindex_type(es, db, doc_type, args.limit)
        try:
            await es.indices.refresh(index="_all")
        except Exception:
            pass
        logger.info("Reindex complete — %d documents indexed", total)
    finally:
        await close_es()


if __name__ == "__main__":
    asyncio.run(main())
