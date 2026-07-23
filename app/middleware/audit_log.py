"""Activity-log capture.

Reads contract C3 out of ``request.scope["aztu_audit"]`` — written by the permission
dependency — after the response has been produced, and writes one row per audited
mutation.

Two properties this middleware must never violate:

1. **An audit failure can never break or roll back a successful mutation.** The row
   is written on its own ``AsyncSessionLocal()``, never the request's session, and
   the whole block is wrapped in ``except Exception``. The mutation has already been
   committed and the response already produced by the time anything here runs.
2. **The request body is never read here.** The only request-derived data is the
   per-route ``label_fields`` whitelist the dependency already copied, so a password
   cannot reach this table even if a future route rule asks for one.
"""

from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

import uuid

from starlette.responses import Response as PlainResponse

from app.core import audit_payload
from app.core.audit_labels import label_from_fields, resolve_target_label
from app.core.auth_dependency import AUDIT_SCOPE_KEY, SECRET_FIELD_NAMES
from app.core.database import AsyncSessionLocal
from app.core.logger import get_logger
from app.models.admin.activity_log import AdminActivityLog

logger = get_logger("aztu.audit")

SKIP_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

# Refresh is excluded deliberately: it fires every ~15 minutes per logged-in tab and
# would bury the real events. Login (success and failure) and logout are kept.
SKIP_PATHS = frozenset({"/health", "/api/auth/refresh", "/api/chat/message"})
SKIP_PREFIXES = ("/static", "/docs", "/redoc", "/openapi")

LOGIN_PATH = "/api/auth/login"

USER_AGENT_MAX_LENGTH = 500

# Only JSON responses are captured. This API answers every mutation with JSON,
# and buffering anything else risks pulling a file download into memory.
CAPTURED_RESPONSE_TYPES = ("application/json",)
USERNAME_MAX_LENGTH = 50
UNKNOWN_USERNAME = "anonymous"


def _client_ip(request: Request) -> Optional[str]:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        # Left-most entry is the originating client.
        ip = forwarded.split(",")[0].strip()
        if ip:
            return ip[:45]
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()[:45]
    client = request.client
    return client.host[:45] if client else None


def _should_skip(request: Request) -> bool:
    if request.method in SKIP_METHODS:
        return True
    path = request.url.path
    if path in SKIP_PATHS:
        return True
    return any(path.startswith(prefix) for prefix in SKIP_PREFIXES)


def _safe_meta(label_fields: Optional[dict]) -> Optional[dict]:
    """Second gate on the whitelist the dependency already applied."""
    if not label_fields:
        return None
    meta = {
        key: value
        for key, value in label_fields.items()
        if key.lower() not in SECRET_FIELD_NAMES
    }
    return meta or None


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if _should_skip(request):
            return await call_next(request)

        # Correlates this log row with the application log and the caller's own
        # records. The column existed but nothing ever populated it.
        request_id = str(uuid.uuid4())
        request.scope["aztu_request_id"] = request_id

        response = await call_next(request)

        # `call_next` hands back a streaming response, so the body has to be
        # drained to be logged — and then handed on as a fresh response, or the
        # client receives nothing. Only JSON is drained; anything else is passed
        # through untouched so downloads keep streaming.
        response_body = None
        content_type = (response.headers.get("content-type") or "").lower()
        if any(ct in content_type for ct in CAPTURED_RESPONSE_TYPES):
            try:
                chunks = [chunk async for chunk in response.body_iterator]
                raw = b"".join(chunks)
                response_body = audit_payload.from_json_bytes(raw)
                response = PlainResponse(
                    content=raw,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception:
                logger.exception("Audit could not buffer the response body")

        response.headers["X-Request-ID"] = request_id

        try:
            await self._record(request, response, response_body, request_id)
        except Exception:
            logger.exception(
                "Audit log write failed for %s %s", request.method, request.url.path
            )
        return response

    async def _record(
        self,
        request: Request,
        response: Response,
        response_body=None,
        request_id: Optional[str] = None,
    ) -> None:
        audit = request.scope.get(AUDIT_SCOPE_KEY)
        status_code = response.status_code
        path = request.url.path

        is_failed_login = path == LOGIN_PATH and status_code == 401

        if audit is None:
            # No rule seeded the context — nothing to log except the one case that
            # never reaches a successful dependency: a rejected login.
            if not is_failed_login:
                return
            audit = {}

        outcome = audit.get("outcome") or "success"
        denied = outcome == "denied"

        if not (denied or is_failed_login or 200 <= status_code < 400):
            return

        action_key = audit.get("action_key")
        if is_failed_login:
            action_key = "auth.login_failed"
            outcome = "denied"
        if not action_key:
            return

        username = audit.get("actor_username")
        if not username and is_failed_login:
            # The one event with no authenticated actor. The username comes from the
            # form the dependency already parsed — never from the raw body here.
            username = (audit.get("label_fields") or {}).get("username")
        username = (username or UNKNOWN_USERNAME)[:USERNAME_MAX_LENGTH]

        target_type = audit.get("target_type")
        target_id = audit.get("target_id")
        label_fields = audit.get("label_fields") or {}

        route = request.scope.get("route")
        route_template = getattr(route, "path", None)

        user_agent = request.headers.get("user-agent")
        if user_agent:
            user_agent = user_agent[:USER_AGENT_MAX_LENGTH]

        async with AsyncSessionLocal() as db:
            target_label = None
            if not denied:
                target_label = await resolve_target_label(db, target_type, target_id)
            if target_label is None:
                target_label = label_from_fields(_safe_meta(label_fields))

            row = AdminActivityLog(
                admin_user_id=audit.get("actor_id"),
                admin_username=username,
                action_key=action_key,
                domain=audit.get("domain") or action_key.partition(".")[0],
                method=request.method,
                path=path,
                route_template=route_template,
                target_type=target_type,
                target_id=target_id,
                target_label=target_label,
                status_code=status_code,
                outcome=outcome,
                ip=_client_ip(request),
                user_agent=user_agent,
                request_id=request_id,
                request_body=audit.get("request_body"),
                response_body=response_body,
                meta=_safe_meta(label_fields),
            )
            db.add(row)
            await db.commit()
