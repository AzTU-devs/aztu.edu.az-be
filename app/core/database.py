from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

# Strip sslmode/channel_binding from URL — passed via connect_args instead
_parsed = urlparse(settings.DATABASE_URL)
_query_params = parse_qs(_parsed.query)
_query_params.pop("sslmode", None)
_query_params.pop("channel_binding", None)
_clean_url = urlunparse(_parsed._replace(query=urlencode(_query_params, doseq=True)))

async_database_url = _clean_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    async_database_url,
    connect_args={"ssl": "require"},
    # Only log SQL in development — never in production (avoids leaking query params)
    echo=settings.ENVIRONMENT == "development",
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


Base = declarative_base()
