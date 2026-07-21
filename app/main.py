import os
import time
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.logger import get_logger
from app.core.rate_limit import limiter
from app.core.auth_dependency import PermissionDenied, enforce_permission
from app.core.permission_map import verify_permission_map
from app.core.rbac_bootstrap import sync_rbac
from app.core.startup import seed_admin_user
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.api_key import PublicApiKeyMiddleware
from app.middleware.audit_log import AuditLogMiddleware

logger = get_logger("aztu.api")

from app.api.v1.router.news import router as news_router
from app.api.v1.router.hero import router as hero_router
from app.api.v1.router.project import router as project_router
from app.api.v1.router.announcement import router as announcement_router
from app.api.v1.router.news_category import router as news_category_router
from app.api.v1.router.faculty import router as faculty_router
from app.api.v1.router.cafedra import router as cafedra_router
from app.api.v1.router.menu import router as menu_router
from app.api.v1.router.menu_header import router as menu_header_router
from app.api.v1.router.collaboration import router as collaboration_router
from app.api.v1.router.auth import router as auth_router
from app.api.v1.router.employee import router as employee_router
from app.api.v1.router.department import router as department_router
from app.api.v1.router.research_institute import router as research_institute_router
from app.api.v1.router.research_project import router as research_project_router
from app.middleware.article import router as article_router
from app.api.v1.router.chat import router as chat_router
from app.api.v1.router.chatbot_knowledge import router as chatbot_knowledge_router
from app.api.v1.router.search import router as search_router
from app.api.v1.router.rbac import router as rbac_router
from app.api.v1.router.admin_user import router as admin_user_router
from app.api.v1.router.activity import router as activity_router
from app.api.v1.router.visits import router as visits_router
from app.api.v1.router.stats import router as stats_router
from app.core.scheduler import start_scheduler, stop_scheduler
from app.core.elasticsearch import get_es, close_es
from app.services.search import ensure_indices


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Order matters: roles/permissions must exist before the map is verified against
    # the catalogue and before the seeded admin can be given the super_admin role.
    await sync_rbac()
    verify_permission_map(app)
    await seed_admin_user()
    # Surfaced at boot rather than only when a visitor gets an unexplained
    # failure — a missing key makes the chatbot 401 in milliseconds, which is
    # indistinguishable from any other 500 at the widget.
    if not settings.OPEN_AI_KEY:
        logger.warning("OPEN_AI_KEY is not set — the chatbot will not answer.")
    start_scheduler()
    try:
        es = await get_es()
        await ensure_indices(es)
    except Exception as exc:
        logger.warning("Elasticsearch unavailable on startup: %s", exc)
    yield
    stop_scheduler()
    await close_es()


app = FastAPI(
    title="AzTU University API",
    description="Backend API for AzTU website (news, announcements, hero, etc.)",
    version="1.0.0",
    lifespan=lifespan,
    # ONE global permission dependency instead of 180 handler edits. Solved after the
    # router has set scope["route"], so (method, route.path) is available for lookup.
    dependencies=[Depends(enforce_permission)],
    docs_url=f"/docs-{settings.DOCS_TOKEN}" if settings.DOCS_TOKEN else None,
    redoc_url=f"/redoc-{settings.DOCS_TOKEN}" if settings.DOCS_TOKEN else None,
    openapi_url=f"/openapi-{settings.DOCS_TOKEN}.json" if settings.DOCS_TOKEN else None,
)

# ── Rate limiting ──────────────────────────────────────────────────────────────
# slowapi backed by Redis: per-route @limiter.limit(...) decorators (e.g. auth
# login 5/min, chat 20/min) and global default_limits enforce DoS protection
# consistently across all uvicorn workers.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ── Security headers ───────────────────────────────────────────────────────────
app.add_middleware(SecurityHeadersMiddleware)

# ── Public GET API-key gate ────────────────────────────────────────────────────
# GET endpoints require X-API-Key, unless the request originates from
# aztu.edu.az (Origin/Referer match). Non-GET endpoints are protected by the
# JWT `require_admin` dependency at the route level.
app.add_middleware(PublicApiKeyMiddleware)

# ── Admin activity log ─────────────────────────────────────────────────────────
# Registered before CORS so that CORS stays the outermost layer and this sits
# inside it: the audit row is written after the route has run and after
# scope["route"] is set, but the response still passes back out through CORS.
# Writes on its own session — an audit failure can never roll back a mutation.
app.add_middleware(AuditLogMiddleware)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Accept-Language"],
)


# ── Request logging middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()
    # slowapi's SlowAPIMiddleware unconditionally reads request.state.view_rate_limit
    # to inject headers; if the limiter check is skipped (exempt route, early error)
    # the attribute is never set and Starlette raises AttributeError. Pre-seed it.
    request.state.view_rate_limit = None
    response = await call_next(request)
    elapsed_ms = (time.monotonic() - start) * 1000
    level = logging.ERROR if response.status_code >= 500 else logging.DEBUG
    logger.log(
        level,
        "%s %s %d %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


from fastapi.encoders import jsonable_encoder

# ... (inside validation_exception_handler)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Request validation failed on %s %s: %s",
        request.method,
        request.url.path,
        exc.errors(),
    )
    if settings.ENVIRONMENT == "production":
        body = {"status_code": 422, "detail": "Invalid request"}
    else:
        body = {"status_code": 422, "detail": exc.errors()}
    return JSONResponse(status_code=422, content=jsonable_encoder(body))


# ── Permission denials (contract C2: flat body, never retried by the FE) ───────
@app.exception_handler(PermissionDenied)
async def permission_denied_handler(request: Request, exc: PermissionDenied):
    return JSONResponse(
        status_code=403,
        content={
            "status_code": 403,
            "detail": exc.detail,
            "required_permission": exc.required_permission,
        },
    )


# ── Global exception handler ───────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception on %s %s", request.method, request.url.path
    )
    return JSONResponse(
        status_code=500,
        content={"status_code": 500, "error": "Internal server error"},
    )


# ── Static files (absolute path prevents working-directory issues) ─────────────
_static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth_router,          prefix="/api/auth",          tags=["Auth"])
app.include_router(news_router,          prefix="/api/news",          tags=["News"])
app.include_router(hero_router,          prefix="/api/hero",          tags=["Hero"])
app.include_router(project_router,       prefix="/api/project",       tags=["Project"])
app.include_router(announcement_router,  prefix="/api/announcement",  tags=["Announcement"])
app.include_router(news_category_router, prefix="/api/news-category", tags=["News Category"])
app.include_router(faculty_router,       prefix="/api/faculty",       tags=["Faculty"])
app.include_router(cafedra_router,       prefix="/api/cafedra",       tags=["Cafedra"])
app.include_router(menu_router,          prefix="/api/menu",          tags=["Menu"])
app.include_router(menu_header_router,   prefix="/api/menu/header",   tags=["Menu Header"])
app.include_router(collaboration_router, prefix="/api/collaboration", tags=["Collaboration"])
app.include_router(employee_router,    prefix="/api/employee",    tags=["Employee"])
app.include_router(department_router,  prefix="/api/department",  tags=["Department"])
app.include_router(research_institute_router, prefix="/api/research-institute", tags=["Research Institute"])
app.include_router(research_project_router,   prefix="/api/research-project",   tags=["Research Project"])
app.include_router(article_router,           prefix="/api/article",           tags=["Article"])
app.include_router(chat_router,              prefix="/api/chat",              tags=["Chat"])
app.include_router(chatbot_knowledge_router, prefix="/api/chatbot-knowledge", tags=["Chatbot Knowledge"])
app.include_router(search_router,            prefix="/api/search",            tags=["Search"])
app.include_router(rbac_router,              prefix="/api",                   tags=["RBAC"])
app.include_router(admin_user_router,        prefix="/api/admin-users",       tags=["Admin Users"])
app.include_router(activity_router,          prefix="/api/activity",          tags=["Activity Log"])
app.include_router(visits_router,            prefix="/api/visits",            tags=["Visits"])
app.include_router(stats_router,             prefix="/api/stats",             tags=["Stats"])


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root():
    index_path = os.path.join(_static_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
