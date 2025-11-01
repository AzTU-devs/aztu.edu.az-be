from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers (create separate files for modular routes)
# from app.routers import news, announcements, users

app = FastAPI(
    title="AzTU University API",
    description="Backend API for AzTU website (news, announcements, sliders, etc.)",
    version="1.0.0"
)

# Allow CORS for frontend (adjust origins to your frontend URL)
origins = [
    "http://localhost:3000",  # React dev server
    "https://aztu.edu.az"     # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to AzTU University API!"}

# Example: Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}