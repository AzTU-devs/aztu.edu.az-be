import os
import ssl
from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# --- Clean URL query params that may force SSL or other pg features your server doesn't support
parsed = urlparse(DATABASE_URL)
query_params = parse_qs(parsed.query)

# Remove SSL-related params if present (we control SSL via connect_args below)
query_params.pop("sslmode", None)
query_params.pop("channel_binding", None)

new_query = urlencode(query_params, doseq=True)
clean_url = urlunparse(parsed._replace(query=new_query))

# Convert sync URL to async SQLAlchemy URL
# Example: postgresql://...  -> postgresql+asyncpg://...
async_database_url = clean_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# --- SSL toggle via env (recommended)
# Docker/local: DB_SSL=0
# Managed cloud DB that requires SSL: DB_SSL=1
USE_SSL = os.getenv("DB_SSL", "0") == "1"

connect_args = {}
if USE_SSL:
    # Use default trusted CAs (good for managed DBs with proper certs)
    connect_args["ssl"] = ssl.create_default_context()
else:
    # Your error: "rejected SSL upgrade" -> disable SSL
    connect_args["ssl"] = False

engine = create_async_engine(
    async_database_url,
    connect_args=connect_args,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
