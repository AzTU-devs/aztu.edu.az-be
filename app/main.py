import os
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
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
from app.core.startup import seed_admin_user
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

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
from app.middleware.article import router as article_router
from app.api.v1.router.chat import router as chat_router
from app.api.v1.router.chatbot_knowledge import router as chatbot_knowledge_router
from app.core.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_admin_user()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title="AzTU University API",
    description="Backend API for AzTU website (news, announcements, hero, etc.)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=f"/docs-{os.getenv('DOCS_TOKEN', '')}" if os.getenv("DOCS_TOKEN") else None,
    redoc_url=f"/redoc-{os.getenv('DOCS_TOKEN', '')}" if os.getenv("DOCS_TOKEN") else None,
    openapi_url=f"/openapi-{os.getenv('DOCS_TOKEN', '')}.json" if os.getenv("DOCS_TOKEN") else None,
)

# ── Rate limiting ──────────────────────────────────────────────────────────────
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# # SlowAPIMiddleware keeps stricter @limiter.limit(...) decorators working
# # (e.g. auth login: 5/min, chat: tighter quotas).
# app.add_middleware(SlowAPIMiddleware)
#
# # Global per-IP rate limit for every /api/* route in api/v1/router/*.
# # 100 requests / minute / IP. /api/auth/* is exempted because auth.py
# # already enforces stricter per-route limits via @limiter.limit.
# app.add_middleware(
#     RateLimitMiddleware,
#     max_requests=100,
#     window_seconds=60,
#     path_prefixes=("/api/",),
#     exempt_paths=("/api/auth/",),
# )

# ── Security headers ───────────────────────────────────────────────────────────
app.add_middleware(SecurityHeadersMiddleware)

# ── CORS ───────────────────────────────────────────────────────────────────────
# allow_origin_regex=".*" allows all origins while remaining compatible with allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ── Request logging middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()
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
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"status_code": 422, "detail": exc.errors()}),
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
app.include_router(article_router,           prefix="/api/article",           tags=["Article"])
app.include_router(chat_router,              prefix="/api/chat",              tags=["Chat"])
app.include_router(chatbot_knowledge_router, prefix="/api/chatbot-knowledge", tags=["Chatbot Knowledge"])


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root():
    index_path = os.path.join(_static_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
