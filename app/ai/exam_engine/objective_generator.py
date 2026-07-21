from __future__ import annotations

import json

from app.ai.client import AIClient
from app.ai.prompts.objective_exam import build_objective_prompt
from app.ai.exam_engine.objective_models import ObjectivePaper


class ObjectiveExamGenerator:

    def __init__(self):

        self.ai = AIClient()

    def generate(
        self,
        analysis,
        material,
        total_questions,
    ) -> ObjectivePaper:

        prompt = build_objective_prompt(
            analysis,
            material,
            total_questions,
        )

        response = self.ai.chat(prompt)

        return ObjectivePaper.model_validate(
            json.loads(response)
        )
