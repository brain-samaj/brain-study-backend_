from __future__ import annotations

from collections.abc import AsyncGenerator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL


# Convert PostgreSQL URL to SQLAlchemy asyncpg URL.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )


# Convert Neon/libpq connection parameters to asyncpg-compatible parameters.
parts = urlsplit(DATABASE_URL)
query = parse_qsl(parts.query, keep_blank_values=True)

clean_query = []

for key, value in query:
    if key == "sslmode":
        clean_query.append(("ssl", "require"))
    elif key == "channel_binding":
        # asyncpg does not accept this libpq parameter.
        continue
    else:
        clean_query.append((key, value))

DATABASE_URL = urlunsplit(
    (
        parts.scheme,
        parts.netloc,
        parts.path,
        urlencode(clean_query),
        parts.fragment,
    )
)


engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
