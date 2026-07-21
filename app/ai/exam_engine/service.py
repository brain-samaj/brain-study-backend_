from __future__ import annotations

import json

from app.ai.client import AIClient
from app.ai.exam_engine.models import TheoryPaper
from app.ai.prompts.theory_exam import build_theory_exam_prompt


class TheoryExamGenerator:

    def __init__(self):

        self.ai = AIClient()

    def generate(
        self,
        analysis,
        material,
        duration,
        answer_any,
    ) -> TheoryPaper:

        prompt = build_theory_exam_prompt(
            analysis,
            material,
            duration,
            answer_any,
        )

        response = self.ai.chat(prompt)

        return TheoryPaper.model_validate(
            json.loads(response)
        )
