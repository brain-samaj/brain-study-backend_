from __future__ import annotations

from datetime import datetime
from datetime import timezone

from app.core.security import create_access_token
from app.core.security import hash_password
from app.core.security import verify_password
from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import AuthResponse
from app.modules.auth.schemas import LoginRequest
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.schemas import UserResponse


class AuthService:
    """
    Authentication business logic.

    Handles:
    - User registration
    - User login
    - User profile retrieval
    """

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register(
        self,
        payload: RegisterRequest,
    ) -> AuthResponse:

        email = payload.email.lower().strip()

        if self.repository.email_exists(email):
            raise ValueError("Email already exists.")

        user = User(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            email=email,
            password_hash=hash_password(payload.password),
            education_level=payload.education_level.strip(),
        )

        user = self.repository.create(user)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=TokenResponse(
                access_token=create_access_token(str(user.id)),
            ),
        )

    def login(
        self,
        payload: LoginRequest,
    ) -> AuthResponse:

        user = self.repository.get_by_email(
            payload.email.lower().strip()
        )

        if user is None:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            payload.password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        user.last_login_at = datetime.now(timezone.utc)
        self.repository.save(user)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=TokenResponse(
                access_token=create_access_token(str(user.id)),
            ),
        )

    def get_current_user(
        self,
        user: User,
    ) -> UserResponse:
        return UserResponse.model_validate(user)
