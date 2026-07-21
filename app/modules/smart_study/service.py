from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.services.smart_study import SmartStudyEngine
from app.modules.smart_study.repository import SmartStudyRepository


class SmartStudyService:
    """
    Orchestrates Smart Study.

    Responsibilities

    • Load learning progress
    • Select next topic
    • Generate question
    • Mark answer
    • Update progress
    """

    def __init__(
        self,
        db: Session,
    ):

        self.repository = SmartStudyRepository(db)

        self.engine = SmartStudyEngine()


    ####################################################
    # START / CONTINUE SESSION
    ####################################################

    async def next_question(
        self,
        *,
        user,
        study_material,
        analysis: dict,
    ):

        summary = self.repository.get_learning_summary(
            user_id=user.id,
            study_material_id=study_material.id,
        )

        learning_state = {
            "difficulty": (
                summary["overall_progress"].difficulty
                if summary["overall_progress"]
                else "adaptive"
            ),
            "weak_topics": summary["weak_topics"],
            "mastered_topics": summary["mastered_topics"],
            "average_accuracy": summary["average_accuracy"],
            "average_response_time": summary["average_response_time"],
        }

        return await self.engine.next_question(
            study_material=study_material,
            analysis=analysis,
            user=user,
            learning_state=learning_state,
        )

    ####################################################
    # SUBMIT ANSWER
    ####################################################

    async def submit_answer(
        self,
        *,
        session,
        question,
        student_answer: str,
    ):

        """
        Full implementation comes after the
        Smart Study router and schemas.

        This method will

        1. Ask AI to mark

        2. Save history

        3. Update topic mastery

        4. Update overall mastery

        5. Return explanation

        6. Generate next question
        """

        raise NotImplementedError

    ####################################################
    # DASHBOARD
    ####################################################

    def dashboard(
        self,
        *,
        user_id: UUID,
        study_material_id: UUID,
    ):

        return self.repository.get_learning_summary(
            user_id=user_id,
            study_material_id=study_material_id,
        )

