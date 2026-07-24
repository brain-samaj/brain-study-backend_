from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.modules.exams.exceptions import ExamExpiredError
from app.modules.exams.models import ExamSession
from app.modules.exams.repository import ExamRepository


class ExamTimerService:
    """
    Server-side Exam Timer Engine.

    Responsibilities
    ----------------
    - Calculate remaining time.
    - Prevent frontend timer manipulation.
    - Expire sessions automatically.
    - Provide timer information to clients.

    The frontend only displays time.
    Backend owns the truth.
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
    ) -> None:

        self._repository = repository


    async def start_timer(
        self,
        session: ExamSession,
    ) -> ExamSession:

        now = datetime.now(
            UTC,
        )

        session.started_at = now

        session.expires_at = (
            now.replace(
                microsecond=0,
            )
        )

        session.expires_at = (
            session.expires_at
            +
            __import__(
                "datetime"
            )
            .timedelta(
                minutes=session.duration_minutes
            )
        )

        await self._repository.update_session(
            session,
        )

        await self._repository.commit()

        return session



    async def get_remaining_time(
        self,
        session_id: UUID,
    ) -> dict:

        session = await (
            self._repository
            .get_session(
                session_id,
            )
        )

        if session is None:

            raise ValueError(
                "Exam session not found."
            )


        now = datetime.now(
            UTC,
        )


        if (
            session.expires_at
            and
            now >= session.expires_at
        ):

            session.status = (
                session.status.EXPIRED
            )

            await self._repository.commit()

            raise ExamExpiredError(
                "Exam time has expired."
            )


        remaining = (
            session.expires_at
            -
            now
        )


        remaining_seconds = max(
            int(
                remaining.total_seconds()
            ),
            0,
        )


        total_seconds = (
            session.duration_minutes
            *
            60
        )


        elapsed = (
            total_seconds
            -
            remaining_seconds
        )


        progress = (
            elapsed
            /
            total_seconds
            *
            100
            if total_seconds
            else 0
        )


        return {
            "started_at": (
                session.started_at
            ),
            "expires_at": (
                session.expires_at
            ),
            "server_time": now,
            "duration_minutes": (
                session.duration_minutes
            ),
            "elapsed_seconds": elapsed,
            "remaining_seconds": remaining_seconds,
            "progress_percent": progress,
            "expired": False,
        }
