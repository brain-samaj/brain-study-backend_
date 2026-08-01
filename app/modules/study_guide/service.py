from __future__ import annotations

from fastapi import HTTPException, status

from app.ai.services.teacher import TeacherAI
from app.modules.knowledge_engine.repository import KnowledgeRepository


class StudyGuideService:
    """
    Generates teacher-quality study guides.

    Workflow

        Upload
            ↓
        Knowledge Engine
            ↓
      Structured Knowledge
            ↓
         TeacherAI
            ↓
       Beautiful Lesson

    The Knowledge Engine performs the educational analysis once.

    TeacherAI NEVER analyses the uploaded material again.
    It teaches ONLY from the stored structured knowledge and
    educational metadata.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ) -> None:
        self.repository = repository
        self.teacher = TeacherAI()

    async def generate(
        self,
        *,
        study_material_id,
        education_level: str,
    ) -> str:

        knowledge = await self.repository.get_by_material(
            material_id=study_material_id,
        )

        if knowledge is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge source not found.",
            )

        status_value = (
            knowledge.status.value
            if hasattr(knowledge.status, "value")
            else str(knowledge.status)
        ).upper()

        if status_value != "READY":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Knowledge source is not ready yet. "
                    f"Current status: {status_value}"
                ),
            )

        if not knowledge.topics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Knowledge has not been generated.",
            )

        analysis: dict = {}

        if isinstance(knowledge.knowledge, dict):
            analysis = knowledge.knowledge.get("analysis", {})
            if not analysis:
                analysis = knowledge.knowledge

        return await self.teacher.generate_study_guide(
            title=knowledge.title,
            subject=analysis.get(
                "subject",
                knowledge.title,
            ),
            education_level=education_level,

            topics=knowledge.topics or [],
            glossary=knowledge.glossary or [],
            learning_objectives=knowledge.learning_objectives or [],
            key_points=knowledge.key_points or [],
            sample_questions=knowledge.sample_questions or [],

            teaching_style=analysis.get(
                "teaching_style",
                "Adaptive",
            ),
            explanation_style=analysis.get(
                "explanation_style",
                "Simple",
            ),
            example_density=analysis.get(
                "example_density",
                "Moderate",
            ),
            reasoning_depth=analysis.get(
                "reasoning_depth",
                "Intermediate",
            ),

            needs_worked_examples=analysis.get(
                "needs_worked_examples",
                False,
            ),
            needs_real_life_examples=analysis.get(
                "needs_real_life_examples",
                False,
            ),
            needs_visual_explanations=analysis.get(
                "needs_visual_explanations",
                False,
            ),
            needs_step_by_step=analysis.get(
                "needs_step_by_step",
                False,
            ),
            needs_definitions_first=analysis.get(
                "needs_definitions_first",
                True,
            ),
            needs_classification=analysis.get(
                "needs_classification",
                False,
            ),
            needs_comparison_tables=analysis.get(
                "needs_comparison_tables",
                False,
            ),
            needs_timelines=analysis.get(
                "needs_timelines",
                False,
            ),
            needs_mnemonics=analysis.get(
                "needs_mnemonics",
                False,
            ),

            requires_formulae=analysis.get(
                "requires_formulae",
                False,
            ),
            requires_calculations=analysis.get(
                "requires_calculations",
                False,
            ),
            requires_tables=analysis.get(
                "requires_tables",
                False,
            ),
            requires_diagrams=analysis.get(
                "requires_diagrams",
                False,
            ),
            requires_code=analysis.get(
                "requires_code",
                False,
            ),
            requires_memorization=analysis.get(
                "requires_memorization",
                False,
            ),

            keywords=analysis.get(
                "keywords",
                [],
            ),
            important_terms=analysis.get(
                "important_terms",
                [],
            ),
            prerequisites=analysis.get(
                "prerequisites",
                [],
            ),

            learning_styles=analysis.get(
                "learning_styles",
                ["mixed"],
            ),
            best_teaching_methods=analysis.get(
                "best_teaching_methods",
                [],
            ),
            common_student_mistakes=analysis.get(
                "common_student_mistakes",
                [],
            ),
            real_world_applications=analysis.get(
                "real_world_applications",
                [],
            ),
            recommended_learning_order=analysis.get(
                "recommended_learning_order",
                [],
            ),
        )
