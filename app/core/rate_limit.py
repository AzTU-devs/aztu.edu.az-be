from starlette.requests import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


def _client_key(request: Request) -> str:
    # uvicorn is configured with --proxy-headers and --forwarded-allow-ips
    # restricted to the trusted reverse proxy (Cloudflare). request.client.host
    # is therefore the real client IP and we don't need to re-read XFF here
    # (which would otherwise be spoofable from the public internet).
    return get_remote_address(request)


# Redis-backed limiter so all uvicorn workers share the same counter state.
# - default_limits: per-IP DoS baseline applied to every request via SlowAPIMiddleware.
# - Stricter @limiter.limit(...) decorators on sensitive routes (login, chat) stack
#   on top of the default limits.
# Production: Redis-backed so all uvicorn workers share counter state.
# Development/tests: in-process memory so the app runs without a Redis instance.
_storage_uri = settings.REDIS_URL if settings.ENVIRONMENT == "production" else "memory://"

limiter = Limiter(
    key_func=_client_key,
    default_limits=["100/minute", "1000/hour"],
    headers_enabled=False,
    storage_uri=_storage_uri,
    # Fail open if storage is briefly unreachable instead of returning 500 to
    # every caller. Storage errors are logged.
    swallow_errors=True,
)
