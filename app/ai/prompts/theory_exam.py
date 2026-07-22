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
- Include define, explain, compare, discuss, evaluate, calculate and analyze questions.
- Cover the entire study material.
- Questions should progressively increase in difficulty.

JSON FORMAT

[
  {{
    "question":"",
    "mark":10,
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

Material

{content}
"""


def build_theory_exam_prompt(
    *,
    analysis,
    material: str,
    duration: int = 120,
    answer_any: int = 5,
) -> str:
    """
    Backward compatibility wrapper.
    Existing services use this function name.
    """

    return TheoryExamPromptBuilder.build(
        subject=analysis.subject,
        topic=analysis.topic,
        duration=duration,
        answer_any=answer_any,
        content=material,
    )
