from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User


class AuthRepository:
    """
    Async repository responsible for User persistence.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        stmt = select(User).where(
            User.id == user_id
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        stmt = (
            select(User)
            .where(
                User.email == email.lower().strip()
            )
            .where(
                User.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


    async def email_exists(
        self,
        email: str,
    ) -> bool:

        user = await self.get_by_email(email)

        return user is not None


    async def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user


    async def update(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user


    async def save(
        self,
        user: User,
    ) -> User:

        return await self.update(user)


    async def delete(
        self,
        user: User,
    ) -> None:

        await self.db.delete(user)

        await self.db.commit()
