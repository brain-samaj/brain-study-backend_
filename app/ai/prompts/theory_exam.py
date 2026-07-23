from __future__ import annotations


class TheoryExamPromptBuilder:

    @staticmethod
    def build(
        *,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        content: str,
    ) -> str:

        return f"""
You are an experienced university examination setter.

Generate a professional THEORY examination.

Rules

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- Questions must require reasoning.
- Cover every important concept from the material.
- Mix define, explain, compare, discuss, calculate,
  evaluate and analyze questions.
- Increase difficulty gradually.
- Every question must include marking guidance.

Return ONLY JSON.

[
  {{
    "question":"",

    "marks":10,

    "difficulty":"medium",

    "expected_points":[
      "",
      "",
      ""
    ],

    "sample_answer":""
  }}
]

Subject:
{subject}

Topic:
{topic}

Difficulty:
{difficulty}

Questions:
{question_count}

Material:

{content}
"""


def build_theory_exam_prompt(
    *,
    analysis,
    material: str,
    total_questions: int,
    difficulty: str = "mixed",
) -> str:

    return TheoryExamPromptBuilder.build(
        subject=analysis.subject,
        topic=analysis.topic,
        difficulty=difficulty,
        question_count=total_questions,
        content=material,
    )
