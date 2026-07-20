import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError

from app.core.session import get_db
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.auth_dependency import AUDIT_SCOPE_KEY, require_admin
from app.models.admin.admin_user import AdminUser
from app.services.rbac import get_role_snapshot

router = APIRouter()
logger = logging.getLogger("aztu.auth")

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH = "/api/auth"


def _mark_audit(request: Request, **fields) -> None:
    """Fill in the actor on the routes where the permission dependency cannot know it.

    Only the username is ever copied — never the body, never the password.
    """
    audit = request.scope.get(AUDIT_SCOPE_KEY)
    if isinstance(audit, dict):
        audit.update(fields)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AdminUser).where(AdminUser.username == body.username)
    )
    user: AdminUser | None = result.scalar_one_or_none()

    # Constant-time path: always run verify even if user not found to prevent timing attacks
    if not user or not verify_password(body.password, user.hashed_password):
        _mark_audit(
            request,
            actor_username=body.username[:255],
            action_key="auth.login_failed",
            outcome="denied",
        )
        logger.warning(
            "Failed login attempt for username=%s ip=%s",
            body.username,
            request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.is_active:
        _mark_audit(
            request,
            actor_username=user.username,
            action_key="auth.login_failed",
            outcome="denied",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)

    # Store hashed refresh token for rotation/revocation
    user.refresh_token_hash = hash_password(refresh_token)
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    _mark_audit(request, actor_id=user.id, actor_username=user.username)

    logger.info(
        "Successful login for username=%s ip=%s",
        user.username,
        request.client.host if request.client else "unknown",
    )

    # Set refresh token as httpOnly Secure SameSite=strict cookie
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path=REFRESH_COOKIE_PATH,
    )

    return TokenResponse(access_token=access_token)


@router.get("/me")
async def me(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: AdminUser = Depends(require_admin),
):
    snapshot = await get_role_snapshot(db, user.role_id)
    role = user.role
    return JSONResponse(
        content={
            "status_code": 200,
            "data": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_image": user.profile_image,
                "is_active": bool(user.is_active),
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
                "role": None if role is None else {
                    "id": role.id,
                    "code": role.code,
                    "name_az": role.name_az,
                    "name_en": role.name_en,
                    "is_system": bool(role.is_system),
                },
                "is_super_admin": bool(snapshot and snapshot.is_super_admin),
                # Empty for a super admin — is_super_admin governs there.
                "permissions": sorted(snapshot.permissions) if snapshot else [],
                # The dashboard's route guard mirrors this: under "audit" it lets a
                # missing permission through so a mis-mapped route cannot lock an
                # admin out of a screen the API would have allowed.
                "enforcement_mode": settings.PERMISSION_ENFORCEMENT_MODE,
            },
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("20/minute")
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Wrong token type")
        username: str = payload["sub"]
    except (JWTError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    result = await db.execute(
        select(AdminUser).where(
            AdminUser.username == username,
            AdminUser.is_active == True,  # noqa: E712
        )
    )
    user: AdminUser | None = result.scalar_one_or_none()
    if not user or not user.refresh_token_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found or revoked",
        )

    # Verify the stored hash matches this refresh token (rotation guard)
    if not verify_password(refresh_token, user.refresh_token_hash):
        # Potential token reuse — invalidate session entirely
        user.refresh_token_hash = None
        await db.commit()
        logger.warning("Refresh token reuse detected for username=%s", username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalidated due to token reuse",
        )

    # Issue new tokens (rotate refresh token)
    new_access_token = create_access_token(user.username)
    new_refresh_token = create_refresh_token(user.username)

    user.refresh_token_hash = hash_password(new_refresh_token)
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=new_refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path=REFRESH_COOKIE_PATH,
    )

    return TokenResponse(access_token=new_access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
):
    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            username = payload.get("sub")
        except (JWTError, ValueError, KeyError):
            username = None
        if username:
            result = await db.execute(
                select(AdminUser).where(AdminUser.username == username)
            )
            user = result.scalar_one_or_none()
            if user:
                user.refresh_token_hash = None
                await db.commit()
                _mark_audit(request, actor_id=user.id, actor_username=user.username)

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
    )
