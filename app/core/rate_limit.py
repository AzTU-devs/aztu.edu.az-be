from starlette.requests import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def _client_key(request: Request) -> str:
    # Honor reverse-proxy headers (nginx / cloudflare) when present so the
    # limiter sees the real client IP, not the proxy's IP.
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return get_remote_address(request)


# Global limiter — applied to every request via SlowAPIMiddleware.
# default_limits = baseline brute-force / DoS protection per IP.
# Stricter limits on sensitive endpoints (login, chat) are set with
# @limiter.limit(...) decorators on those routes.
limiter = Limiter(
    key_func=_client_key,
    default_limits=["100/minute", "1000/hour"],
    headers_enabled=True,
)
