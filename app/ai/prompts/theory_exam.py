from app.ai.analyzers.models import DocumentAnalysis


def build_theory_exam_prompt(
    analysis: DocumentAnalysis,
    material: str,
    duration: int,
    answer_any: int,
):

    if answer_any >= 10:
        total = 12
    else:
        total = answer_any + 2

    return f"""
You are a senior university lecturer.

Create a REAL university examination paper.

Subject

{analysis.subject}

Topic

{analysis.topic}

Duration

{duration} minutes

Students must answer

ANY {answer_any} QUESTIONS.

Generate

{total} COMPLETE QUESTIONS.

Each question MUST contain

(a)

(b)

(c)

(d)

Each sub-question must have marks.

Each question must contain a hidden detailed marking guide.

The paper must resemble a real university examination.

Questions must become progressively harder.

Calculation questions where appropriate.

Essay questions where appropriate.

Case studies where appropriate.

Never repeat concepts.

Return ONLY JSON.

Material

{material}
"""
