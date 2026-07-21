from __future__ import annotations

from app.ai.services.study_guide_generator import StudyGuideGenerator
from app.ai.services.flashcard_generator import FlashcardGenerator
from app.ai.services.smart_study import SmartStudyEngine
from app.ai.services.exam_generator import ExamGenerator


class AIOrchestrator:

    def __init__(self):

        self.study_guide = StudyGuideGenerator()

        self.flashcards = FlashcardGenerator()

        self.smart_study = SmartStudyEngine()

        self.exam = ExamGenerator()


    async def build_learning_pack(
        self,
        *,
        subject: str,
        title: str,
        material: str,
        education_level: str,
    ):

        guide = await self.study_guide.generate(
            subject=subject,
            title=title,
            material=material,
            education_level=education_level,
        )

        flashcards = await self.flashcards.generate(
            subject=subject,
            study_material=material,
            study_guide=str(guide),
        )

        return {
            "study_guide": guide,
            "flashcards": flashcards,
        }


    async def generate_exam(
        self,
        *,
        subject: str,
        study_material: str,
        study_guide: str,
        question_type: str,
        questions: int,
    ):

        return await self.exam.generate_exam(
            subject=subject,
            study_material=study_material,
            study_guide=study_guide,
            question_type=question_type,
            requested_questions=questions,
        )


    async def next_smart_study_question(
        self,
        *,
        subject: str,
        study_material: str,
        study_guide: str,
        previous_questions: list,
        previous_answers: list,
    ):

        return await self.smart_study.next_question(
            subject=subject,
            study_material=study_material,
            study_guide=study_guide,
            previous_questions=previous_questions,
            previous_answers=previous_answers,
        )

