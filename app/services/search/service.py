"""Elasticsearch indexing + search for AzTU primary content models.

Indexing helpers re-query the DB by primary identifier so callers in service
files only need a single line after `db.commit()` and don't have to pass
loaded relationships around. All ES errors are caught and logged — they
must NEVER fail the originating API request.
"""

from __future__ import annotations

import logging
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError

from app.core.config import settings
from app.services.search.mappings import LANG_TO_ANALYZER, index_settings
from app.services.search.indexers import (
    build_news_doc,
    build_announcement_doc,
    build_project_doc,
    build_collaboration_doc,
    build_faculty_doc,
    build_cafedra_doc,
    build_department_doc,
    build_employee_doc,
    build_research_institute_doc,
)

logger = logging.getLogger("aztu.search")

SUPPORTED_LANGS = ("az", "en", "ru")
DOC_TYPES = (
    "news",
    "announcement",
    "project",
    "collaboration",
    "faculty",
    "cafedra",
    "department",
    "employee",
    "research_institute",
)


def index_name(doc_type: str, lang: str) -> str:
    return f"{settings.SEARCH_INDEX_PREFIX}_{doc_type}_{lang}"


def alias_name(lang: str) -> str:
    return f"{settings.SEARCH_INDEX_PREFIX}_search_{lang}"


# ── Index lifecycle ──────────────────────────────────────────────────────────

async def ensure_indices(es: AsyncElasticsearch) -> None:
    """Create all per-type per-language indices and language aliases if missing."""
    for lang in SUPPORTED_LANGS:
        analyzer = LANG_TO_ANALYZER.get(lang, "standard")
        body = index_settings(analyzer)
        for doc_type in DOC_TYPES:
            name = index_name(doc_type, lang)
            try:
                exists = await es.indices.exists(index=name)
                if not exists:
                    await es.indices.create(index=name, body=body)
                    logger.info("Created ES index %s", name)
            except Exception as exc:
                logger.warning("ensure_indices: index %s failed: %s", name, exc)
                continue
            # Attach to per-language alias
            try:
                alias = alias_name(lang)
                has_alias = await es.indices.exists_alias(name=alias, index=name)
                if not has_alias:
                    await es.indices.put_alias(index=name, name=alias)
            except Exception as exc:
                logger.warning("ensure_indices: alias for %s failed: %s", name, exc)


async def drop_indices(es: AsyncElasticsearch, doc_types: Iterable[str] | None = None,
                      langs: Iterable[str] | None = None) -> None:
    types = tuple(doc_types) if doc_types else DOC_TYPES
    langs_t = tuple(langs) if langs else SUPPORTED_LANGS
    for lang in langs_t:
        for doc_type in types:
            try:
                await es.indices.delete(index=index_name(doc_type, lang))
            except NotFoundError:
                pass
            except Exception as exc:
                logger.warning("drop_indices: %s_%s failed: %s", doc_type, lang, exc)


# ── Document write helpers ───────────────────────────────────────────────────

async def _safe_index(es: AsyncElasticsearch, doc_type: str, lang: str, doc_id, body: dict) -> None:
    try:
        await es.index(
            index=index_name(doc_type, lang),
            id=str(doc_id),
            document=body,
            refresh="false",
        )
    except Exception as exc:
        logger.warning("ES index %s/%s/%s failed: %s", doc_type, lang, doc_id, exc)


async def _safe_delete(es: AsyncElasticsearch, doc_type: str, lang: str, doc_id) -> None:
    try:
        await es.delete(index=index_name(doc_type, lang), id=str(doc_id), refresh="false")
    except NotFoundError:
        return
    except Exception as exc:
        logger.warning("ES delete %s/%s/%s failed: %s", doc_type, lang, doc_id, exc)


async def delete_doc_by_type(es: AsyncElasticsearch, doc_type: str, doc_id) -> None:
    """Delete a doc from every language index for a given type."""
    for lang in SUPPORTED_LANGS:
        await _safe_delete(es, doc_type, lang, doc_id)


# ── Per-type reindex (queries DB by id, builds per-language docs) ────────────

async def reindex_news(es: AsyncElasticsearch, db: AsyncSession, news_id: int) -> None:
    from app.models.news.news import News
    from app.models.news.news_translation import NewsTranslation

    news = (await db.execute(select(News).where(News.news_id == news_id))).scalar_one_or_none()
    if not news:
        await delete_doc_by_type(es, "news", news_id)
        return
    translations = (await db.execute(
        select(NewsTranslation).where(NewsTranslation.news_id == news_id)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        tr = tr_by_lang.get(lang)
        doc = build_news_doc(news, tr, lang)
        if doc is None:
            await _safe_delete(es, "news", lang, news_id)
        else:
            await _safe_index(es, "news", lang, news_id, doc)


async def reindex_announcement(es: AsyncElasticsearch, db: AsyncSession, announcement_id: int) -> None:
    from app.models.announcement.announcement import Announcement
    from app.models.announcement.announcement_translation import AnnouncementTranslation

    ann = (await db.execute(
        select(Announcement).where(Announcement.announcement_id == announcement_id)
    )).scalar_one_or_none()
    if not ann:
        await delete_doc_by_type(es, "announcement", announcement_id)
        return
    translations = (await db.execute(
        select(AnnouncementTranslation).where(AnnouncementTranslation.announcement_id == announcement_id)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_announcement_doc(ann, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "announcement", lang, announcement_id)
        else:
            await _safe_index(es, "announcement", lang, announcement_id, doc)


async def reindex_project(es: AsyncElasticsearch, db: AsyncSession, project_id: int) -> None:
    from app.models.project.project import Project
    from app.models.project.project_tr import ProjectTranslation

    proj = (await db.execute(
        select(Project).where(Project.project_id == project_id)
    )).scalar_one_or_none()
    if not proj:
        await delete_doc_by_type(es, "project", project_id)
        return
    translations = (await db.execute(
        select(ProjectTranslation).where(ProjectTranslation.project_id == project_id)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_project_doc(proj, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "project", lang, project_id)
        else:
            await _safe_index(es, "project", lang, project_id, doc)


async def reindex_collaboration(es: AsyncElasticsearch, db: AsyncSession, collaboration_id: int) -> None:
    from app.models.collaboration.collaboration import Collaboration
    from app.models.collaboration.collaboration_tr import CollaborationTranslation

    coll = (await db.execute(
        select(Collaboration).where(Collaboration.collaboration_id == collaboration_id)
    )).scalar_one_or_none()
    if not coll:
        await delete_doc_by_type(es, "collaboration", collaboration_id)
        return
    translations = (await db.execute(
        select(CollaborationTranslation).where(CollaborationTranslation.collaboration_id == collaboration_id)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_collaboration_doc(coll, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "collaboration", lang, collaboration_id)
        else:
            await _safe_index(es, "collaboration", lang, collaboration_id, doc)


async def reindex_faculty(es: AsyncElasticsearch, db: AsyncSession, faculty_code: str) -> None:
    from app.models.faculties.faculties import Faculty
    from app.models.faculties.faculties_tr import FacultyTr

    fac = (await db.execute(
        select(Faculty).where(Faculty.faculty_code == faculty_code)
    )).scalar_one_or_none()
    if not fac:
        await delete_doc_by_type(es, "faculty", faculty_code)
        return
    translations = (await db.execute(
        select(FacultyTr).where(FacultyTr.faculty_code == faculty_code)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_faculty_doc(fac, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "faculty", lang, faculty_code)
        else:
            await _safe_index(es, "faculty", lang, faculty_code, doc)


async def reindex_cafedra(es: AsyncElasticsearch, db: AsyncSession, cafedra_code: str) -> None:
    from app.models.cafedras.cafedras import Cafedra
    from app.models.cafedras.cafedras_tr import CafedraTr

    caf = (await db.execute(
        select(Cafedra).where(Cafedra.cafedra_code == cafedra_code)
    )).scalar_one_or_none()
    if not caf:
        await delete_doc_by_type(es, "cafedra", cafedra_code)
        return
    translations = (await db.execute(
        select(CafedraTr).where(CafedraTr.cafedra_code == cafedra_code)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_cafedra_doc(caf, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "cafedra", lang, cafedra_code)
        else:
            await _safe_index(es, "cafedra", lang, cafedra_code, doc)


async def reindex_department(es: AsyncElasticsearch, db: AsyncSession, department_code: str) -> None:
    from app.models.departments.department import Department
    from app.models.departments.department_tr import DepartmentTr

    dep = (await db.execute(
        select(Department).where(Department.department_code == department_code)
    )).scalar_one_or_none()
    if not dep:
        await delete_doc_by_type(es, "department", department_code)
        return
    translations = (await db.execute(
        select(DepartmentTr).where(DepartmentTr.department_code == department_code)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_department_doc(dep, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "department", lang, department_code)
        else:
            await _safe_index(es, "department", lang, department_code, doc)


async def reindex_employee(es: AsyncElasticsearch, db: AsyncSession, employee_code: str) -> None:
    from app.models.employee.employee import Employee
    from app.models.employee.employee_tr import EmployeeTr

    emp = (await db.execute(
        select(Employee).where(Employee.employee_code == employee_code)
    )).scalar_one_or_none()
    if not emp:
        await delete_doc_by_type(es, "employee", employee_code)
        return
    translations = (await db.execute(
        select(EmployeeTr).where(EmployeeTr.employee_code == employee_code)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_employee_doc(emp, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "employee", lang, employee_code)
        else:
            await _safe_index(es, "employee", lang, employee_code, doc)


async def reindex_research_institute(es: AsyncElasticsearch, db: AsyncSession, institute_code: str) -> None:
    from app.models.research_institute.institute import ResearchInstitute, ResearchInstituteTr

    inst = (await db.execute(
        select(ResearchInstitute).where(ResearchInstitute.institute_code == institute_code)
    )).scalar_one_or_none()
    if not inst:
        await delete_doc_by_type(es, "research_institute", institute_code)
        return
    translations = (await db.execute(
        select(ResearchInstituteTr).where(ResearchInstituteTr.institute_code == institute_code)
    )).scalars().all()
    tr_by_lang = {t.lang_code: t for t in translations}
    for lang in SUPPORTED_LANGS:
        doc = build_research_institute_doc(inst, tr_by_lang.get(lang), lang)
        if doc is None:
            await _safe_delete(es, "research_institute", lang, institute_code)
        else:
            await _safe_index(es, "research_institute", lang, institute_code, doc)


# ── Hook helpers (one line per service-file call site) ──────────────────────

async def _hook(reindex_fn, db, ident) -> None:
    """Run an async reindex inside a guarded ES client lookup."""
    try:
        from app.core.elasticsearch import get_es as _get_es
        es = await _get_es()
    except Exception as exc:
        logger.warning("ES client unavailable for indexing: %s", exc)
        return
    try:
        await reindex_fn(es, db, ident)
    except Exception as exc:
        logger.warning("Reindex hook %s(%s) failed: %s", reindex_fn.__name__, ident, exc)


async def _delete_hook(doc_type: str, ident) -> None:
    try:
        from app.core.elasticsearch import get_es as _get_es
        es = await _get_es()
    except Exception as exc:
        logger.warning("ES client unavailable for delete: %s", exc)
        return
    try:
        await delete_doc_by_type(es, doc_type, ident)
    except Exception as exc:
        logger.warning("Delete hook %s(%s) failed: %s", doc_type, ident, exc)


async def on_news_change(db, news_id):                 await _hook(reindex_news, db, news_id)
async def on_news_delete(news_id):                     await _delete_hook("news", news_id)
async def on_announcement_change(db, announcement_id): await _hook(reindex_announcement, db, announcement_id)
async def on_announcement_delete(announcement_id):     await _delete_hook("announcement", announcement_id)
async def on_project_change(db, project_id):           await _hook(reindex_project, db, project_id)
async def on_project_delete(project_id):               await _delete_hook("project", project_id)
async def on_collaboration_change(db, collaboration_id): await _hook(reindex_collaboration, db, collaboration_id)
async def on_collaboration_delete(collaboration_id):   await _delete_hook("collaboration", collaboration_id)
async def on_faculty_change(db, faculty_code):         await _hook(reindex_faculty, db, faculty_code)
async def on_faculty_delete(faculty_code):             await _delete_hook("faculty", faculty_code)
async def on_cafedra_change(db, cafedra_code):         await _hook(reindex_cafedra, db, cafedra_code)
async def on_cafedra_delete(cafedra_code):             await _delete_hook("cafedra", cafedra_code)
async def on_department_change(db, department_code):   await _hook(reindex_department, db, department_code)
async def on_department_delete(department_code):       await _delete_hook("department", department_code)
async def on_employee_change(db, employee_code):       await _hook(reindex_employee, db, employee_code)
async def on_employee_delete(employee_code):           await _delete_hook("employee", employee_code)
async def on_research_institute_change(db, institute_code): await _hook(reindex_research_institute, db, institute_code)
async def on_research_institute_delete(institute_code):     await _delete_hook("research_institute", institute_code)


# ── Search ───────────────────────────────────────────────────────────────────

async def search(
    es: AsyncElasticsearch,
    query: str,
    lang: str = "az",
    types: Iterable[str] | None = None,
    limit: int = 8,
) -> dict:
    """Multi-search across the per-language alias, grouped by type.

    Returns a dict shaped like:
        {
          "results": { "news": [...], "faculty": [...], ... },
          "total": <int>,
          "degraded": <bool>   # true when ES query failed
        }
    """
    if lang not in SUPPORTED_LANGS:
        lang = "az"
    selected = tuple(t for t in (types or DOC_TYPES) if t in DOC_TYPES)
    if not selected:
        selected = DOC_TYPES

    # Build a multi-search body — one search per type so each can be limited
    # independently. Querying the per-language alias filtered by `type` keeps
    # mappings/analyzers consistent.
    msearch_body: list[dict] = []
    for doc_type in selected:
        msearch_body.append({"index": index_name(doc_type, lang)})
        msearch_body.append({
            "size": limit,
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^3", "snippet", "extra"],
                                "type": "best_fields",
                                "fuzziness": "AUTO",
                            }
                        }
                    ],
                    "filter": [{"term": {"type": doc_type}}],
                }
            },
            "highlight": {
                "fields": {
                    "title": {"number_of_fragments": 0},
                    "snippet": {"fragment_size": 140, "number_of_fragments": 1},
                }
            },
        })

    try:
        resp = await es.msearch(searches=msearch_body)
    except Exception as exc:
        logger.warning("ES search failed: %s", exc)
        return {"results": {t: [] for t in selected}, "total": 0, "degraded": True}

    results: dict[str, list[dict]] = {}
    total = 0
    for doc_type, response in zip(selected, resp.get("responses", [])):
        hits_block = response.get("hits", {}) if isinstance(response, dict) else {}
        hits = hits_block.get("hits", [])
        results[doc_type] = []
        for h in hits:
            src = h.get("_source", {}) or {}
            highlight = h.get("highlight", {}) or {}
            results[doc_type].append({
                "id": src.get("id"),
                "type": src.get("type", doc_type),
                "lang": src.get("lang", lang),
                "title": (highlight.get("title") or [src.get("title")])[0],
                "snippet": (highlight.get("snippet") or [src.get("snippet")])[0],
                "url": src.get("url"),
                "image": src.get("image"),
                "score": h.get("_score"),
            })
            total += 1
    return {"results": results, "total": total, "degraded": False}
