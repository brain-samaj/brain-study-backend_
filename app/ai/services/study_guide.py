from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts import RICH_OUTPUT_PROMPT
from app.ai.services.question_strategy import QuestionStrategy


class StudyGuideGenerator:
    """
    Generates an adaptive Study Guide from uploaded material.

    The guide is never generic. It adapts to the subject,
    difficulty, education level and document content.
    """

    def __init__(self):

        self.ai = AIClient()

        self.strategy = QuestionStrategy()

    async def generate(
        self,
        *,
        study_material,
        user,
        analysis: dict,
    ):

        plan = self.strategy.build_generation_plan(
            analysis=analysis,
            education_level=user.education_level,
            total_questions=20,
            difficulty=analysis.get(
                "Difficulty",
                "adaptive",
            ),
        )

        prompt = self.build_prompt(
            study_material=study_material,
            analysis=analysis,
            plan=plan,
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
    ) -> str:

        return f"""
{RICH_OUTPUT_PROMPT}

You are Brain Study AI.

Generate a COMPLETE university study guide.

Do NOT summarize.

Teach the student as if they are attending a lecture.

======================================

Subject

{analysis["Subject"]}

Main Topic

{analysis["Main Topic"]}

Sub Topics

{analysis["Sub Topics"]}

Difficulty

{analysis["Difficulty"]}

Learning Style

{analysis["Learning Style"]}

======================================

Generation Plan

{plan}

======================================


Subject Teaching Strategy

{self.subject_instructions(analysis)}

Requirements

Teach every concept progressively.

Do not skip difficult concepts.

Use simple language first.

Gradually increase complexity.

Every explanation must come from the uploaded material.

Never invent facts.

======================================

If formulas exist

Return equations in LaTeX.

======================================

If calculations exist

Provide complete worked examples.

======================================

If diagrams help

Return diagram blocks.

======================================

If tables improve understanding

Return table blocks.

======================================

Always include

Introduction

Learning Objectives

Core Concepts

Worked Examples

Common Mistakes

Memory Tips

Real-world Applications

Practice Questions

Exam Tips

Conclusion

======================================

Return ONLY LearningDocument JSON.

Study Material

{study_material.extracted_text[:25000]}
"""

    def subject_instructions(
        self,
        analysis: dict,
    ) -> str:

        subject = analysis.get(
            "Subject",
            "",
        ).lower()

        ########################################################
        # MATHEMATICS
        ########################################################

        if "math" in subject:

            return """
Teach as a mathematics professor.

Every formula must use LaTeX.

Every difficult concept must include:

• theorem

• proof when appropriate

• worked example

• exam shortcut

• common mistakes

Avoid long paragraphs.
"""

        ########################################################
        # PHYSICS
        ########################################################

        if "physics" in subject:

            return """
Teach as a physics lecturer.

Include

• equations

• derivations

• worked calculations

• SI units

• practical applications

• assumptions
"""

        ########################################################
        # CHEMISTRY
        ########################################################

        if "chemistry" in subject:

            return """
Teach like a chemistry lecturer.

Include

• balanced equations

• mechanisms

• reactions

• calculations

• laboratory notes

• safety notes
"""

        ########################################################
        # BIOLOGY
        ########################################################

        if "biology" in subject:

            return """
Teach with diagrams.

Explain processes step-by-step.

Highlight functions.

Highlight differences.

Return diagram blocks whenever possible.
"""

        ########################################################
        # LAW
        ########################################################

        if "law" in subject:

            return """
Teach like a law professor.

Explain

• legal principles

• statutes

• precedents

• case analysis

• examination techniques
"""

        ########################################################
        # ACCOUNTING
        ########################################################

        if "accounting" in subject:

            return """
Teach using

• journal entries

• ledgers

• financial statements

• worked solutions

• examination adjustments
"""

        ########################################################
        # COMPUTER SCIENCE
        ########################################################

        if "computer" in subject:

            return """
Teach using

• algorithms

• syntax

• code examples

• optimisation

• debugging

Return code blocks.
"""

        ########################################################
        # DEFAULT
        ########################################################

        return """
Teach progressively.

Start from beginner level.

Move to advanced level.

Use examples frequently.
"""


