from __future__ import annotations

import json

from app.ai.client import AIClient


class KnowledgeBuilder:

    def __init__(self):
        self.ai = AIClient()


    async def build(
        self,
        *,
        subject: str,
        title: str,
        material: str,
    ) -> dict:

        prompt = f"""
You are an expert educational knowledge engineer.

Convert this learning material into structured knowledge.

Subject

{subject}

Title

{title}

Material

{material}

Extract ONLY information contained in the material.

Return JSON with the following structure.

{{
  "subject":"",
  "title":"",
  "difficulty":"",
  "topics":[],
  "subtopics":[],
  "definitions":[],
  "principles":[],
  "laws":[],
  "formulas":[],
  "equations":[],
  "symbols":[],
  "constants":[],
  "processes":[],
  "algorithms":[],
  "proofs":[],
  "worked_examples":[],
  "examples":[],
  "applications":[],
  "advantages":[],
  "disadvantages":[],
  "comparisons":[],
  "mnemonics":[],
  "common_mistakes":[],
  "exam_tips":[],
  "keywords":[]
}}

Return ONLY JSON.
"""

        response = await self.ai.generate_json(prompt)

        return json.loads(response)

