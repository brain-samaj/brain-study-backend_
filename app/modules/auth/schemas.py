from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    education_level: str = Field(
        min_length=2,
        max_length=100,
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    first_name: str

    last_name: str

    email: EmailStr

    education_level: str

    avatar_url: str | None = None

    is_active: bool

    is_verified: bool


class TokenResponse(BaseModel):
    access_token: str

    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: UserResponse

    token: TokenResponse


class MessageResponse(BaseModel):
    message: str
