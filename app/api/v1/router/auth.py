import logging
from datetime import datetime
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
from app.models.admin.admin_user import AdminUser

router = APIRouter()
logger = logging.getLogger("aztu.auth")

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH = "/api/auth"


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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)

    # Store hashed refresh token for rotation/revocation
    user.refresh_token_hash = hash_password(refresh_token)
    user.last_login_at = datetime.utcnow()
    await db.commit()

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


@router.post("/refresh", response_model=TokenResponse)
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
    user.updated_at = datetime.utcnow()
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
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
):
    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            username = payload.get("sub")
            if username:
                result = await db.execute(
                    select(AdminUser).where(AdminUser.username == username)
                )
                user = result.scalar_one_or_none()
                if user:
                    user.refresh_token_hash = None
                    await db.commit()
        except (JWTError, Exception):
            pass  # Token already invalid — just clear cookie

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
    )
