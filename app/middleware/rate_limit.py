import time
from collections import deque
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Per-IP sliding-window rate limiter.

    Applies to every request whose path starts with one of `path_prefixes`
    (default: /api/). Each IP is allowed `max_requests` per `window_seconds`.
    On exceed: 429 with Retry-After.

    Storage is in-process memory — fine for single-worker dev/test. For
    production with multiple workers, swap to Redis.
    """

    def __init__(
        self,
        app,
        max_requests: int = 50,
        window_seconds: int = 60,
        path_prefixes: tuple[str, ...] = ("/api/",),
        exempt_paths: tuple[str, ...] = ("/api/auth/",),  # auth has its own stricter limit
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.path_prefixes = path_prefixes
        self.exempt_paths = exempt_paths
        self._hits: dict[str, deque[float]] = {}
        self._lock = Lock()

    def _client_ip(self, request: Request) -> str:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()
        return request.client.host if request.client else "unknown"

    def _should_limit(self, path: str) -> bool:
        if not any(path.startswith(p) for p in self.path_prefixes):
            return False
        if any(path.startswith(p) for p in self.exempt_paths):
            return False
        return True

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method == "OPTIONS" or not self._should_limit(request.url.path):
            return await call_next(request)

        ip = self._client_ip(request)
        now = time.monotonic()
        cutoff = now - self.window

        with self._lock:
            dq = self._hits.get(ip)
            if dq is None:
                dq = deque()
                self._hits[ip] = dq
            while dq and dq[0] < cutoff:
                dq.popleft()

            if len(dq) >= self.max_requests:
                retry_after = max(1, int(dq[0] + self.window - now))
                return JSONResponse(
                    status_code=429,
                    content={
                        "status_code": 429,
                        "error": "Too Many Requests",
                        "detail": f"Rate limit: {self.max_requests} requests per {self.window}s",
                        "retry_after": retry_after,
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(self.max_requests),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + retry_after),
                    },
                )

            dq.append(now)
            remaining = self.max_requests - len(dq)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = f"{self.window}s"
        return response
