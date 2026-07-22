from __future__ import annotations


class DocumentAnalysisPromptBuilder:

    @staticmethod
    def build(
        *,
        title: str,
        content: str,
    ) -> str:

        return f"""
You are one of the world's best educators and curriculum designers.

Your task is NOT to summarize.

Your task is to deeply analyze the learning material.

Return ONLY valid JSON.

Required JSON format:

{{
    "title":"",
    "subject":"",
    "topic":"",
    "difficulty":"",
    "language":"",
    "education_level":"",
    "estimated_reading_minutes":0,
    "word_count":0,

    "requires_calculations":false,
    "requires_formulae":false,
    "requires_tables":false,
    "requires_diagrams":false,
    "requires_code":false,
    "requires_memorization":false,

    "keywords":[
    ],

    "learning_objectives":[
    ],

    "important_terms":[
    ],

    "prerequisites":[
    ],

    "learning_style":"",
    "confidence":0.0
}}

Rules

Detect the actual subject.

Detect the exact topic.

Estimate the educational level.

Estimate the reading duration.

Determine if formulas exist.

Determine if calculations exist.

Determine if diagrams are necessary.

Determine if programming code exists.

Determine if heavy memorization is required.

Extract all major concepts.

Extract important terminology.

Extract learning objectives.

Extract prerequisite knowledge.

Choose ONE learning style:

visual

practical

mathematical

reading

mixed

Confidence must be between 0 and 1.

Document Title

{title}

Document Content

{content}
"""
