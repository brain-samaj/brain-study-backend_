from app.ai.analyzers.models import DocumentAnalysis


def build_objective_prompt(
    analysis: DocumentAnalysis,
    material: str,
    total_questions: int,
):

    return f"""
You are an experienced university examination lecturer.

Generate {total_questions} multiple-choice questions.

Subject

{analysis.subject}

Topic

{analysis.topic}

Rules

Questions must cover the whole material.

Difficulty should gradually increase.

Never repeat concepts.

Each question must have

A

B

C

D

Exactly ONE correct answer.

Include explanation.

Include difficulty.

Include topic.

Calculation questions when necessary.

Programming questions when necessary.

Clinical questions when necessary.

Return ONLY JSON.

Material

{material}
"""
