from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to every HTTP response.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Support for Private Network Access (PNA)
        # Required when a global domain (public) requests a local IP (private)
        if request.headers.get("access-control-request-private-network") == "true":
            response.headers["Access-Control-Allow-Private-Network"] = "true"

        # Skip other security headers for CORS preflight (OPTIONS)
        if request.method == "OPTIONS":
            return response

        # Prevent MIME-type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking (allow same-origin for internal tools if needed, but DENY is safer)
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS filter
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Enforce HTTPS for 1 year (only if secure)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # Restrict referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Relax or remove CSP for public-facing API to avoid cross-origin issues during early development
        # response.headers["Content-Security-Policy"] = ...

        return response
