import logging
from elasticsearch import AsyncElasticsearch

from app.core.config import settings

logger = logging.getLogger("aztu.elasticsearch")

_es_client: AsyncElasticsearch | None = None


def _build_client() -> AsyncElasticsearch:
    auth = None
    if settings.ELASTICSEARCH_USERNAME and settings.ELASTICSEARCH_PASSWORD:
        auth = (settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD)
    return AsyncElasticsearch(
        hosts=[settings.ELASTICSEARCH_URL],
        basic_auth=auth,
        request_timeout=10,
        max_retries=2,
        retry_on_timeout=True,
    )


async def get_es() -> AsyncElasticsearch:
    global _es_client
    if _es_client is None:
        _es_client = _build_client()
    return _es_client


async def close_es() -> None:
    global _es_client
    if _es_client is not None:
        try:
            await _es_client.close()
        except Exception as exc:
            logger.warning("Elasticsearch close failed: %s", exc)
        _es_client = None
