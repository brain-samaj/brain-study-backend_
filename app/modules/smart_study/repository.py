from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.smart_study.models import SmartStudyProgress
from app.modules.smart_study.topic_progress_models import TopicProgress
from app.modules.smart_study.question_history_models import (
    SmartStudyQuestionHistory,
)


class SmartStudyRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    ########################################################
    # OVERALL PROGRESS
    ########################################################

    def get_progress(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> SmartStudyProgress | None:

        return (
            self.db.execute(
                select(
                    SmartStudyProgress,
                ).where(
                    SmartStudyProgress.user_id == user_id,
                    SmartStudyProgress.study_material_id == study_material_id,
                )
            )
            .scalars()
            .first()
        )

    def save_progress(
        self,
        progress: SmartStudyProgress,
    ) -> SmartStudyProgress:

        self.db.add(progress)

        self.db.commit()

        self.db.refresh(progress)

        return progress

    ########################################################
    # TOPIC PROGRESS
    ########################################################

    def get_topic_progress(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
        topic: str,
    ) -> TopicProgress | None:

        return (
            self.db.execute(
                select(
                    TopicProgress,
                ).where(
                    TopicProgress.user_id == user_id,
                    TopicProgress.study_material_id == study_material_id,
                    TopicProgress.topic == topic,
                )
            )
            .scalars()
            .first()
        )

    def save_topic_progress(
        self,
        progress: TopicProgress,
    ) -> TopicProgress:

        self.db.add(progress)

        self.db.commit()

        self.db.refresh(progress)

        return progress

    def list_topics(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> list[TopicProgress]:

        return (
            self.db.execute(
                select(
                    TopicProgress,
                ).where(
                    TopicProgress.user_id == user_id,
                    TopicProgress.study_material_id == study_material_id,
                )
            )
            .scalars()
            .all()
        )


    ########################################################
    # QUESTION HISTORY
    ########################################################

    def save_question(
        self,
        question: SmartStudyQuestionHistory,
    ) -> SmartStudyQuestionHistory:

        self.db.add(question)

        self.db.commit()

        self.db.refresh(question)

        return question

    def recent_questions(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
        limit: int = 20,
    ) -> list[SmartStudyQuestionHistory]:

        return (
            self.db.execute(
                select(
                    SmartStudyQuestionHistory,
                )
                .where(
                    SmartStudyQuestionHistory.user_id == user_id,
                    SmartStudyQuestionHistory.study_material_id == study_material_id,
                )
                .order_by(
                    SmartStudyQuestionHistory.created_at.desc(),
                )
                .limit(limit)
            )
            .scalars()
            .all()
        )

    def update_question(
        self,
        question: SmartStudyQuestionHistory,
    ) -> SmartStudyQuestionHistory:

        self.db.add(question)

        self.db.commit()

        self.db.refresh(question)

        return question

    ########################################################
    # LEARNING ANALYTICS
    ########################################################

    def get_weak_topics(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
        threshold: float = 0.60,
    ) -> list[TopicProgress]:

        return (
            self.db.execute(
                select(TopicProgress)
                .where(
                    TopicProgress.user_id == user_id,
                    TopicProgress.study_material_id == study_material_id,
                    TopicProgress.mastery_score < threshold,
                )
                .order_by(
                    TopicProgress.mastery_score.asc(),
                )
            )
            .scalars()
            .all()
        )

    def get_mastered_topics(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
        threshold: float = 0.85,
    ) -> list[TopicProgress]:

        return (
            self.db.execute(
                select(TopicProgress)
                .where(
                    TopicProgress.user_id == user_id,
                    TopicProgress.study_material_id == study_material_id,
                    TopicProgress.mastery_score >= threshold,
                )
                .order_by(
                    TopicProgress.mastery_score.desc(),
                )
            )
            .scalars()
            .all()
        )

    def get_topic_accuracy(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
        topic: str,
    ) -> float:

        progress = self.get_topic_progress(
            user_id=user_id,
            study_material_id=study_material_id,
            topic=topic,
        )

        if progress is None:

            return 0.0

        if progress.total_questions == 0:

            return 0.0

        return (
            progress.correct_answers
            / progress.total_questions
        )

    def get_average_accuracy(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> float:

        progress = self.get_progress(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        if progress is None:

            return 0.0

        if progress.total_questions == 0:

            return 0.0

        return (
            progress.correct_answers
            / progress.total_questions
        )

    def get_average_response_time(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> float:

        topics = self.list_topics(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        if not topics:

            return 0.0

        total = sum(
            topic.average_response_time
            for topic in topics
        )

        return total / len(topics)

    def get_recommended_next_topic(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> TopicProgress | None:

        weak = self.get_weak_topics(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        if weak:

            return weak[0]

        topics = self.list_topics(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        if topics:

            return min(
                topics,
                key=lambda x: x.mastery_score,
            )

        return None

    def get_learning_summary(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ) -> dict:

        progress = self.get_progress(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        topics = self.list_topics(
            user_id=user_id,
            study_material_id=study_material_id,
        )

        return {
            "overall_progress": progress,
            "topic_count": len(topics),
            "average_accuracy": self.get_average_accuracy(
                user_id=user_id,
                study_material_id=study_material_id,
            ),
            "average_response_time": self.get_average_response_time(
                user_id=user_id,
                study_material_id=study_material_id,
            ),
            "weak_topics": [
                topic.topic
                for topic in self.get_weak_topics(
                    user_id=user_id,
                    study_material_id=study_material_id,
                )
            ],
            "mastered_topics": [
                topic.topic
                for topic in self.get_mastered_topics(
                    user_id=user_id,
                    study_material_id=study_material_id,
                )
            ],
        }

