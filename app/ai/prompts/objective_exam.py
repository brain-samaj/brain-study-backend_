"""
Brain Study Objective Exam Prompt.

The AI should ONLY generate question content.
The backend is responsible for numbering, marks,
difficulty, explanations and other metadata.
"""

OBJECTIVE_EXAM_PROMPT = """
You are an expert university examination setter.

Generate high-quality multiple-choice questions using ONLY the supplied study material.

========================
STUDY MATERIAL
========================

{study_content}

========================
SETTINGS
========================

Difficulty:
{difficulty}

Number of questions:
{question_count}

Generate EXACTLY {question_count} questions.

========================
RULES
========================

- Use ONLY the supplied material.
- Do NOT invent facts.
- Every question must have exactly FOUR options.
- Exactly ONE option must be correct.
- Shuffle the correct answer naturally.
- Do NOT include numbering.
- Do NOT include explanations.
- Do NOT include marks.
- Do NOT include topic.
- Do NOT include difficulty.
- Do NOT include any extra fields.

Return ONLY valid JSON.

The JSON MUST follow this schema exactly:

{{
  "questions": [
    {{
      "question": "...",
      "options": [
        "...",
        "...",
        "...",
        "..."
      ],
      "correct_answer": "A"
    }}
  ]
}}

IMPORTANT

- Return ONLY JSON.
- No markdown.
- No code fences.
- No text before JSON.
- No text after JSON.
"""
