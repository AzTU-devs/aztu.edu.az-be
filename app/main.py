import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router.project import router as project_router
from fastapi.staticfiles import StaticFiles

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

app = FastAPI(
    title="AzTU University API",
    description="Backend API for AzTU website (news, announcements, sliders, etc.)",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "https://aztu.edu.az"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(project_router, prefix="/api/project", tags=["Project"])

@app.get("/")
async def root():
    return {"message": "Welcome to AzTU University API!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}