from __future__ import annotations

import json

from app.ai.client import AIClient


class StudyGuideGenerator:

    def __init__(self):
        self.ai = AIClient()


    async def generate(
        self,
        *,
        subject: str,
        title: str,
        material: str,
        education_level: str,
    ) -> dict:

        analysis = await self._analyse_material(
            subject=subject,
            title=title,
            material=material,
        )

        prompt = self._build_prompt(
            subject=subject,
            title=title,
            material=material,
            education_level=education_level,
            analysis=analysis,
        )

        response = await self.ai.generate_json(prompt)

        return json.loads(response)


    async def _analyse_material(
        self,
        *,
        subject: str,
        title: str,
        material: str,
    ):

        prompt = f"""
You are an expert curriculum analyst.

Analyse this learning material.

Subject:
{subject}

Title:
{title}

Material:
{material}

Determine:

- Main topic
- Subtopics
- Difficulty
- Subject category
- Whether calculations are required
- Whether derivations are required
- Whether proofs are required
- Whether diagrams are important
- Whether worked examples are necessary
- Whether memorisation is important
- Whether definitions are important
- Whether formulas are important

Return ONLY JSON.
"""

        response = await self.ai.generate_json(prompt)

        return json.loads(response)


    def _build_prompt(
        self,
        *,
        subject,
        title,
        material,
        education_level,
        analysis,
    ):

        return f"""
You are one of the world's best university lecturers.

Teach this topic exactly the way a brilliant lecturer would.

Student Level:
{education_level}

Subject:
{subject}

Title:
{title}

Material:
{material}

Analysis:
{json.dumps(analysis)}

IMPORTANT

Never generate a generic summary.

Instead build a complete study guide.

The AI MUST decide what sections are needed.

Examples

If Mathematics

Include

 Formula derivations

 Worked examples

 Step-by-step calculations

 Practice examples

If Physics

Include

 Concepts

 Laws

 Formula derivations

 Numerical examples

If Programming

Include

 Code examples

 Best practices

 Common mistakes

If Biology

Include

 Processes

 Diagrams

 Memory tricks

If Chemistry

Include

 Reactions

 Equations

 Worked calculations where applicable

If Law

Include

 Cases

 Principles

 Interpretation

If Literature

Include

 Themes

 Characters

 Analysis

If Economics

Include

 Graphs

 Applications

 Real-world examples

Always include

Introduction

Core explanations

Examples

Exam tips

Common mistakes

Memory aids

Mini recap

Do not explain topics that are not present.

Return ONLY JSON.
"""
