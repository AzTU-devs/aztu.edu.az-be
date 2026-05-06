from urllib.parse import urlparse

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import settings

# Paths exempted from the API-key check (docs, static, health, root, auth flow).
_EXEMPT_PREFIXES: tuple[str, ...] = (
    "/static",
    "/api/auth",
)
_EXEMPT_PATHS: frozenset[str] = frozenset({"/", "/health"})


def _host_is_exempt(header_value: str | None) -> bool:
    if not header_value:
        return False
    host = urlparse(header_value).hostname
    if not host:
        return False
    return host.lower() in {h.lower() for h in settings.PUBLIC_API_KEY_EXEMPT_HOSTS}


class PublicApiKeyMiddleware(BaseHTTPMiddleware):
    """
    Require X-API-Key on GET requests, unless the request originates from a
    whitelisted domain (aztu.edu.az). Non-GET endpoints are protected by the
    JWT `require_admin` dependency on each route and are not handled here.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method != "GET":
            return await call_next(request)

        path = request.url.path
        if path in _EXEMPT_PATHS or path.startswith(_EXEMPT_PREFIXES):
            return await call_next(request)

        # Allow randomized docs paths if configured.
        if settings.DOCS_TOKEN and (
            path == f"/docs-{settings.DOCS_TOKEN}"
            or path == f"/redoc-{settings.DOCS_TOKEN}"
            or path == f"/openapi-{settings.DOCS_TOKEN}.json"
        ):
            return await call_next(request)

        if _host_is_exempt(request.headers.get("origin")) or _host_is_exempt(
            request.headers.get("referer")
        ):
            return await call_next(request)

        if not settings.PUBLIC_API_KEY:
            return JSONResponse(
                status_code=503,
                content={"status_code": 503, "detail": "Public API key not configured"},
            )

        provided = request.headers.get("x-api-key")
        if not provided or provided != settings.PUBLIC_API_KEY:
            return JSONResponse(
                status_code=401,
                content={"status_code": 401, "detail": "Missing or invalid API key"},
            )

        return await call_next(request)
