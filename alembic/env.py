import os
import ssl
import sys
from logging.config import fileConfig
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.database import Base

# Import models so Alembic can see them
from app.models.announcement.announcement import Announcement  # noqa: F401
from app.models.announcement.announcement_translation import AnnouncementTranslation  # noqa: F401
from app.models.news.news import News  # noqa: F401
from app.models.news.news_translation import NewsTranslation  # noqa: F401
from app.models.news_category.news_category import NewsCategory  # noqa: F401
from app.models.news_category.news_category_translation import NewsCategoryTranslation  # noqa: F401
from app.models.news_gallery.news_gallery import NewsGallery  # noqa: F401
from app.models.project.project import Project  # noqa: F401
from app.models.project.project_tr import ProjectTranslation  # noqa: F401
from app.models.slider.slider import Slider  # noqa: F401
from app.models.slider.slider_tr import SliderTranslation  # noqa: F401

load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _build_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    parsed = urlparse(database_url)
    query_params = parse_qs(parsed.query)

    # clean params that sometimes appear on hosted DB URLs
    query_params.pop("sslmode", None)
    query_params.pop("channel_binding", None)

    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))

    return clean_url.replace("postgresql://", "postgresql+asyncpg://")


def _connect_args() -> dict:
    """
    Local docker postgres usually doesn't support SSL.
    Enable SSL only when DB_SSL=1.
    """
    use_ssl = os.getenv("DB_SSL", "0") == "1"
    if not use_ssl:
        return {}
    return {"ssl": ssl.create_default_context()}


def run_migrations_offline() -> None:
    url = _build_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    # make sure sqlalchemy.url is set (we set it below in online mode)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=_connect_args(),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    url = _build_database_url()
    config.set_main_option("sqlalchemy.url", url)

    import asyncio
    asyncio.run(run_migrations_online())
