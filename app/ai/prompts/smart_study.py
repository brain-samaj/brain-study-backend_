from app.ai.analyzers.models import DocumentAnalysis


def build_prompt(
    analysis: DocumentAnalysis,
    text: str,
    previous: list[str],
) -> str:

    return f"""
You are Brain Study's adaptive tutor.

Generate ONLY ONE question.

Subject

{analysis.subject}

Topic

{analysis.topic}

Difficulty

Adaptive.

Already Asked

{previous}

Rules

Never repeat a previous question.

Question must come ONLY from the uploaded material.

If Mathematics or Physics

Generate calculation questions.

If Programming

Generate debugging or code questions.

If Biology

Generate process questions.

If Medicine

Generate clinical questions.

If History

Generate reasoning questions.

If Law

Generate scenario questions.

If Literature

Generate interpretation questions.

Immediately include

Correct answer

Explanation

Return ONLY JSON

Material

{text}
"""
