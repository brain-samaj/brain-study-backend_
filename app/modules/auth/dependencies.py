from __future__ import annotations

from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.database.async_session import get_async_db
from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_auth_repository(
    db: AsyncSession = Depends(get_async_db),
) -> AuthRepository:
    """
    Dependency that provides an async authentication repository.
    """

    return AuthRepository(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: AuthRepository = Depends(get_auth_repository),
) -> User:
    """
    Resolve and return the authenticated user from a Bearer access token.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired authentication token.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


    try:
        payload = decode_token(token)

    except Exception as exc:
        raise credentials_exception from exc


    if payload.get("type") != "access":
        raise credentials_exception


    subject = payload.get("sub")

    if not subject:
        raise credentials_exception


    try:
        user_id = UUID(subject)

    except ValueError as exc:
        raise credentials_exception from exc


    user = await repository.get_by_id(user_id)


    if user is None:
        raise credentials_exception


    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is disabled.",
        )


    return user
