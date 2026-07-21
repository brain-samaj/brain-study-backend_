from __future__ import annotations

import json

from app.ai.client import AIClient


class TheoryMarker:

    def __init__(self):
        self.ai = AIClient()


    async def mark_theory_answer(
        self,
        *,
        question,
        student_answer: str,
    ) -> dict:

        prompt = f"""
You are an experienced university examiner.

You MUST mark exactly according to the marking guide.

Never give marks based on feelings.

Question

{question.question}

Official Marking Guide

{json.dumps(question.marking_scheme, indent=2)}

Maximum Marks

{question.marks}

Student Answer

{student_answer}

Instructions

1. Compare ONLY with the marking guide.

2. Award partial marks where appropriate.

3. Do not award marks for irrelevant points.

4. Ignore spelling mistakes unless they change meaning.

5. Reward equivalent correct explanations.

6. Return detailed feedback.

7. Suggest how the student could improve.

Return ONLY JSON.

{
    "score":0,
    "feedback":"",
    "strengths":[],
    "mistakes":[],
    "missing_points":[],
    "model_answer":""
}
"""

        response = await self.ai.generate_json(prompt)

        result = json.loads(response)

        score = float(result["score"])

        if score < 0:
            score = 0

        if score > question.marks:
            score = float(question.marks)

        result["score"] = score

        return result

