from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import BaseModel


class LearningSession(BaseModel):
    """
    Active Smart Study session.
    """

    __tablename__ = "learning_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    study_material_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "study_materials.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        index=True,
    )

    current_topic: Mapped[str | None] = mapped_column(
        String(255),
    )

    current_subtopic: Mapped[str | None] = mapped_column(
        String(255),
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        default="adaptive",
    )

    questions_answered: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    correct_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wrong_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


########################################################
# LEARNING SESSION
########################################################

def get_active_session(
    self,
    *,
    user_id: UUID,
    study_material_id: UUID,
):

    return (
        self.db.execute(
            select(
                LearningSession,
            ).where(
                LearningSession.user_id == user_id,
                LearningSession.study_material_id == study_material_id,
                LearningSession.is_completed.is_(False),
            )
        )
        .scalars()
        .first()
    )


def create_session(
    self,
    session: LearningSession,
):

    self.db.add(session)

    self.db.commit()

    self.db.refresh(session)

    return session


def update_session(
    self,
    session: LearningSession,
):

    self.db.add(session)

    self.db.commit()

    self.db.refresh(session)

    return session

session = self.repository.get_active_session(
    user_id=user.id,
    study_material_id=study_material.id,
)

if session is None:

    session = self.repository.create_session(
        LearningSession(
            user_id=user.id,
            study_material_id=study_material.id,
            difficulty="adaptive",
        )
    )
