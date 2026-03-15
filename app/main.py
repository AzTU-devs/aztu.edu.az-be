import os
import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import get_logger

logger = get_logger("aztu.api")
from app.api.v1.router.news import router as news_router
from app.api.v1.router.hero import router as hero_router
from app.api.v1.router.project import router as project_router
from app.api.v1.router.announcement import router as announcement_router
from app.api.v1.router.news_category import router as news_category_router
from app.api.v1.router.faculty import router as faculty_router
from app.api.v1.router.cafedra import router as cafedra_router
from app.api.v1.router.menu import router as menu_router
from app.api.v1.router.collaboration import router as collaboration_router

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

app = FastAPI(
    title="AzTU University API",
    description="Backend API for AzTU website (news, announcements, hero, etc.)",
    version="1.0.0"
)

# origins = [
#     "http://localhost:5173",
#     "https://aztu.edu.az",
#     "http://aztu.karamshukurlu.site/",
#     "localhost",
#     "localhost:3000"
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_500_responses(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    elapsed_ms = (time.monotonic() - start) * 1000
    if response.status_code >= 500:
        logger.error(
            "500 | %s %s | %.1fms",
            request.method,
            request.url.path,
            elapsed_ms,
        )
    return response

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(news_router, prefix="/api/news", tags=["News"])
app.include_router(hero_router, prefix="/api/hero", tags=["Hero"])
app.include_router(project_router, prefix="/api/project", tags=["Project"])
app.include_router(announcement_router, prefix="/api/announcement", tags=["Announcement"])
app.include_router(news_category_router, prefix="/api/news-category", tags=["News Category"])
app.include_router(faculty_router, prefix="/api/faculty", tags=["Faculty"])
app.include_router(cafedra_router, prefix="/api/cafedra", tags=["Cafedra"])
app.include_router(menu_router, prefix="/api/menu", tags=["Menu"])
app.include_router(collaboration_router, prefix="/api/collaboration", tags=["Collaboration"])

@app.get("/")
async def root():
    return {"message": "Welcome to AzTU University API!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
