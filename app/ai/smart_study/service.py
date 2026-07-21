from __future__ import annotations

import json

from app.ai.client import AIClient
from app.ai.prompts.smart_study import build_prompt
from app.ai.smart_study.models import StudyQuestion


class SmartStudyService:

    def __init__(self):

        self.ai = AIClient()

    def next_question(
        self,
        analysis,
        material,
        previous_questions,
    ) -> StudyQuestion:

        prompt = build_prompt(
            analysis,
            material,
            previous_questions,
        )

        response = self.ai.chat(prompt)

        return StudyQuestion.model_validate(
            json.loads(response)
        )
