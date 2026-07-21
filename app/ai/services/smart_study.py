from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts import RICH_OUTPUT_PROMPT
from app.ai.services.question_strategy import QuestionStrategy


class SmartStudyEngine:
    """
    Adaptive AI tutor.

    Unlike exams, Smart Study never ends.

    It continuously generates questions,
    evaluates the student's understanding,
    explains mistakes,
    and adjusts difficulty.
    """

    def __init__(self):

        self.ai = AIClient()

        self.strategy = QuestionStrategy()

    async def next_question(
        self,
        *,
        study_material,
        analysis: dict,
        user,
        learning_state: dict,
    ):

        plan = self.strategy.build_generation_plan(
            analysis=analysis,
            education_level=user.education_level,
            total_questions=1,
            difficulty=learning_state.get(
                "difficulty",
                "adaptive",
            ),
        )

        prompt = self.build_prompt(
            study_material=study_material,
            analysis=analysis,
            plan=plan,
            learning_state=learning_state,
        )

        return await self.ai.generate_json(
            prompt,
        )

    def build_prompt(
        self,
        *,
        study_material,
        analysis: dict,
        plan: dict,
        learning_state: dict,
    ) -> str:

        return f"""
{RICH_OUTPUT_PROMPT}

You are Brain Study AI.

You are NOT generating an exam.

You are tutoring a university student.

======================================

Subject

{analysis["Subject"]}

Main Topic

{analysis["Main Topic"]}

Sub Topics

{analysis["Sub Topics"]}

======================================

Student Progress

{learning_state}

======================================

Rules

Generate exactly ONE question.

Never say

Question 1

Question 2

Question 3

Never show numbering.

Never show score.

Never mention remaining questions.

The student should simply feel
the conversation continues naturally.

======================================

After every answer

Return

Correct Answer

Detailed Explanation

Why the chosen answer is wrong (if applicable)

Study Tip

Difficulty

Topic

Learning Objective

======================================

If calculations are required

Return complete worked solutions.

======================================

If formulas exist

Return LaTeX.

======================================

If diagrams help

Return diagram blocks.

======================================

Question types may include

Definition

Application

Scenario

Calculation

Diagram interpretation

Code analysis

Case study

Never repeat previous questions.

Return ONLY LearningDocument JSON.

Study Material

{study_material.extracted_text[:25000]}
"""

