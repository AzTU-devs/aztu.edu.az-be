from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to every HTTP response.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Private Network Access (PNA) — only honor the client request if the
        # operator has explicitly opted in. Reflecting it back automatically
        # would let a public site issue authenticated requests against the
        # local network of users sitting behind this server.
        if (
            settings.ALLOW_PRIVATE_NETWORK_ACCESS
            and request.headers.get("access-control-request-private-network") == "true"
        ):
            response.headers["Access-Control-Allow-Private-Network"] = "true"

        # Skip other security headers for CORS preflight (OPTIONS)
        if request.method == "OPTIONS":
            return response

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), microphone=(), camera=(), payment=()",
        )

        # CSP: the API serves JSON and a single static landing page mounted at /.
        # `default-src 'none'` is safe for JSON responses; the landing page only
        # needs same-origin assets, so 'self' covers it. Swagger UI / ReDoc are
        # served from randomized paths and load assets from jsdelivr, so they
        # need a relaxed policy.
        path = request.url.path
        is_docs = path.startswith("/docs-") or path.startswith("/redoc-")
        is_static = path.startswith("/static/")

        if is_static:
            # Uploaded documents (PDFs) and images are embedded — e.g. the
            # regulatory-documents inline preview <iframe> — by the public web
            # front-ends, which run on their own origins. X-Frame-Options can
            # only say DENY/SAMEORIGIN, so we omit it here and use the CSP
            # frame-ancestors directive to allow exactly the configured
            # front-end origins (plus self) to frame these assets. Everything
            # else stays framing-denied.
            frame_ancestors = " ".join(["'self'", *settings.ALLOWED_ORIGINS])
            response.headers["Content-Security-Policy"] = (
                f"frame-ancestors {frame_ancestors}"
            )
        elif is_docs:
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Content-Security-Policy"] = (
                "default-src 'none'; "
                "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.redoc.ly; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "font-src 'self' data: https://fonts.gstatic.com; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net blob:; "
                "worker-src 'self' blob:; "
                "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"
            )
        else:
            response.headers["X-Frame-Options"] = "DENY"
            response.headers.setdefault(
                "Content-Security-Policy",
                "default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
                "script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'",
            )

        # Enforce HTTPS for 1 year (only if secure)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response
