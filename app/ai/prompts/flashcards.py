from app.ai.analyzers.models import DocumentAnalysis


def build_prompt(
    analysis: DocumentAnalysis,
    material: str,
) -> str:

    return f"""
You are an expert educator.

Create intelligent flashcards.

Subject

{analysis.subject}

Topic

{analysis.topic}

Difficulty

{analysis.difficulty}

Rules

Create high-quality flashcards.

Never create duplicate cards.

One fact per card.

If Mathematics

Front = Question or Formula

Back = Complete explanation and worked solution.

If Physics

Include units and formulas.

If Biology

Front = Process or Structure

Back = Complete explanation.

If Programming

Front = Code or Concept

Back = Explanation and example.

If History

Front = Event

Back = Explanation, significance and date.

If Law

Front = Principle

Back = Meaning and application.

If Chemistry

Include reactions where necessary.

Return ONLY JSON.

Material

{material}
"""
