from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts import RICH_OUTPUT_PROMPT


class AnswerEvaluator:

    def __init__(self):

        self.ai = AIClient()

    async def evaluate(
        self,
        *,
        question,
        student_answer: str,
    ):

        prompt = f"""
{RICH_OUTPUT_PROMPT}

You are an experienced university examiner.

Evaluate the student's answer.

Question

{question.question}

Official Answer

{question.answer}

Student Answer

{student_answer}

Instructions

Evaluate fairly.

Award partial marks where deserved.

Explain every deduction.

Return JSON only.

Return

score

max_score

percentage

grade

passed

strengths

mistakes

missing_points

feedback

model_answer

recommended_revision_topics

confidence
"""

        return await self.ai.generate_json(prompt)

