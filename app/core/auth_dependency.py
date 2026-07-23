"""Authentication + the single global permission dependency.

``enforce_permission`` is registered once on the app (``FastAPI(dependencies=[...])``)
rather than on 180 handlers. App-level dependencies are solved after the router has
set ``scope["route"]``, so ``(method, route.path)`` is available for the map lookup.

The resolved actor is cached in ``scope["aztu_admin_user"]``; ``require_admin`` reads
it back, so every one of the 131 existing call sites keeps working and the request
still costs a single user query.
"""

import logging
from typing import Any, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core import audit_payload
from app.core.audit_payload import SECRET_FIELD_NAMES  # re-exported
from app.core.config import settings
from app.core.permission_map import ROUTE_PERMISSIONS, RouteRule
from app.core.security import decode_token
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.rbac import has_permission

logger = logging.getLogger("aztu.auth")

# auto_error=False: with auto_error=True a *missing* Authorization header yields 403,
# which the front-end interceptor must never refresh on. Missing credentials are an
# authentication failure and must be 401.
bearer_scheme = HTTPBearer(auto_error=False)

ACTOR_SCOPE_KEY = "aztu_admin_user"
AUDIT_SCOPE_KEY = "aztu_audit"

SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
FORM_CONTENT_TYPES = ("multipart/form-data", "application/x-www-form-urlencoded")
LABEL_VALUE_MAX_LENGTH = 200

# `SECRET_FIELD_NAMES` lives in `audit_payload` (imported above) alongside the
# rest of the redaction rules, and is re-exported here because the permission
# layer and the audit middleware both reach for it via this module.

_UNAUTHORIZED = {"WWW-Authenticate": "Bearer"}
_FORBIDDEN_MESSAGE = "Bu əməliyyat üçün icazəniz yoxdur."


class PermissionDenied(HTTPException):
    """403 with the flat body shape the admin axios interceptor expects (contract C2)."""

    def __init__(self, required_permission: Optional[str]):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=_FORBIDDEN_MESSAGE)
        self.required_permission = required_permission


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=_UNAUTHORIZED
    )


def _bearer_token(request: Request) -> Optional[str]:
    header = request.headers.get("Authorization") or ""
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


async def _load_active_admin(db: AsyncSession, token: str) -> AdminUser:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise ValueError("Wrong token type")
        username: str = payload["sub"]
    except (JWTError, ValueError, KeyError):
        raise _unauthorized("Invalid or expired token")

    result = await db.execute(
        select(AdminUser).where(
            AdminUser.username == username,
            AdminUser.is_active == True,  # noqa: E712
        )
    )
    user = result.scalar_one_or_none()
    if not user:
        raise _unauthorized("User not found or inactive")
    return user


async def resolve_actor(request: Request, db: AsyncSession) -> AdminUser:
    """Return the authenticated admin, reusing the one already resolved this request."""
    cached = request.scope.get(ACTOR_SCOPE_KEY)
    if cached is not None:
        return cached

    token = _bearer_token(request)
    if not token:
        raise _unauthorized("Not authenticated")

    user = await _load_active_admin(db, token)
    request.scope[ACTOR_SCOPE_KEY] = user
    return user


async def _label_fields(request: Request, rule: RouteRule) -> dict:
    """Copy the route's whitelisted form fields. Never reads a JSON body, never raises."""
    if not rule.label_fields:
        return {}

    content_type = (request.headers.get("content-type") or "").lower()
    if not any(ct in content_type for ct in FORM_CONTENT_TYPES):
        return {}

    try:
        form = await request.form()
    except Exception:
        return {}

    out = {}
    for field in rule.label_fields:
        if field in SECRET_FIELD_NAMES:
            continue
        value = form.get(field)
        if isinstance(value, str) and value.strip():
            out[field] = value.strip()[:LABEL_VALUE_MAX_LENGTH]
    return out


async def _capture_request_body(request: Request) -> Optional[Any]:
    """Sanitised copy of what the caller sent, for the activity log.

    Read here rather than in the audit middleware for one reason: at this point
    Starlette caches the body on the request, so the route handler still parses
    it normally afterwards. The middleware runs outside that cache and consuming
    the stream there would starve the handler.

    File uploads are summarised, never buffered — see `audit_payload`.
    """
    content_type = (request.headers.get("content-type") or "").lower()

    if any(ct in content_type for ct in FORM_CONTENT_TYPES):
        try:
            form = await request.form()
        except Exception:
            return None
        fields, files = {}, []
        for key, value in form.multi_items():
            if hasattr(value, "filename"):
                files.append(
                    {
                        "field": key,
                        "filename": getattr(value, "filename", None),
                        "content_type": getattr(value, "content_type", None),
                        "size": getattr(getattr(value, "file", None), "tell", lambda: None)(),
                    }
                )
            else:
                fields[key] = str(value)[:LABEL_VALUE_MAX_LENGTH]
        return audit_payload.from_form(fields, files)

    if "json" not in content_type:
        return None

    try:
        raw = await request.body()
    except Exception:
        return None
    return audit_payload.from_json_bytes(raw)


async def _seed_audit_ctx(request: Request, user: Optional[AdminUser], rule: RouteRule) -> None:
    """Write contract C3 into the raw scope so the audit middleware can read it."""
    if rule.no_audit:
        return

    target_id = None
    if rule.target_param:
        if rule.target_source == "query":
            target_id = request.query_params.get(rule.target_param)
        else:
            target_id = (request.scope.get("path_params") or {}).get(rule.target_param)

    request.scope[AUDIT_SCOPE_KEY] = {
        "actor_id": user.id if user else None,
        "actor_username": user.username if user else None,
        "action_key": rule.action_key,
        "domain": rule.domain,
        "target_type": rule.target_type,
        "target_id": str(target_id) if target_id is not None else None,
        "label_fields": await _label_fields(request, rule),
        "request_body": await _capture_request_body(request),
        "outcome": "success",
    }


async def enforce_permission(request: Request, db: AsyncSession = Depends(get_db)) -> None:
    route = request.scope.get("route")
    path = getattr(route, "path", "")
    rule = ROUTE_PERMISSIONS.get((request.method, path))

    if rule is None:
        # Reads without an explicit entry stay public — the API-key middleware governs them.
        if request.method in SAFE_METHODS:
            return
        # Unreachable in practice: verify_permission_map() refuses to boot on an
        # unmapped mutation. In audit mode we still let it through, because an
        # unmapped route is exactly the mapping mistake audit mode exists to survive.
        logger.critical("Unmapped mutating route %s %s", request.method, path)
        if settings.PERMISSION_ENFORCEMENT_MODE == "enforce":
            raise PermissionDenied(None)
        return

    if rule.public:
        await _seed_audit_ctx(request, None, rule)
        return

    user = await resolve_actor(request, db)
    await _seed_audit_ctx(request, user, rule)

    if rule.authenticated_only:
        return

    if await has_permission(db, user, rule.key):
        return

    audit = request.scope.get(AUDIT_SCOPE_KEY)
    if audit is not None:
        audit["outcome"] = "denied"

    logger.warning(
        "Permission denied: user=%s permission=%s route=%s %s mode=%s",
        user.username, rule.key, request.method, path, settings.PERMISSION_ENFORCEMENT_MODE,
    )

    if settings.PERMISSION_ENFORCEMENT_MODE == "enforce":
        raise PermissionDenied(rule.key)


async def require_admin(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> AdminUser:
    """
    FastAPI dependency that validates the Bearer JWT and returns the active AdminUser.
    Attach as `_: AdminUser = Depends(require_admin)` on every write endpoint.
    """
    cached = request.scope.get(ACTOR_SCOPE_KEY)
    if cached is not None:
        return cached

    if credentials is None or (credentials.scheme or "").lower() != "bearer":
        raise _unauthorized("Not authenticated")

    user = await _load_active_admin(db, credentials.credentials)
    request.scope[ACTOR_SCOPE_KEY] = user
    return user
