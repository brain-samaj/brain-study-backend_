from __future__ import annotations

from datetime import datetime, timezone

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    """
    Authentication business logic.

    Handles:
    - User registration
    - User login
    - User profile retrieval
    """

    def __init__(
        self,
        repository: AuthRepository,
    ) -> None:
        self.repository = repository


    async def register(
        self,
        payload: RegisterRequest,
    ) -> AuthResponse:

        email = payload.email.lower().strip()

        if await self.repository.email_exists(email):
            raise ValueError("Email already exists.")


        user = User(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            email=email,
            password_hash=hash_password(
                payload.password
            ),
            education_level=payload.education_level.strip(),
        )


        user = await self.repository.create(user)


        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=TokenResponse(
                access_token=create_access_token(
                    str(user.id)
                ),
            ),
        )


    async def login(
        self,
        payload: LoginRequest,
    ) -> AuthResponse:

        user = await self.repository.get_by_email(
            payload.email.lower().strip()
        )


        if user is None:
            raise ValueError(
                "Invalid email or password."
            )


        if not verify_password(
            payload.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )


        user.last_login_at = datetime.now(
            timezone.utc
        )


        await self.repository.save(user)


        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=TokenResponse(
                access_token=create_access_token(
                    str(user.id)
                ),
            ),
        )


    async def get_current_user(
        self,
        user: User,
    ) -> UserResponse:

        return UserResponse.model_validate(user)
