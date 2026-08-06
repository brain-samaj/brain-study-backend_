"""
Brain Study Theory Exam Prompt.

The AI should ONLY generate question content.
The backend is responsible for numbering, instructions,
marks, labels and other metadata.
"""

THEORY_EXAM_PROMPT = """
You are an expert university examination paper setter.

Generate THEORY examination questions ONLY from the supplied study material.

========================
STUDY MATERIAL
========================

{study_content}

========================
SETTINGS
========================

Difficulty:
{difficulty}

Student should answer:
{question_count} questions.

Generate MORE questions than requested.

If question_count is 5 or less,
generate question_count + 1 questions.

Otherwise,
generate question_count + 2 questions.

========================
RULES
========================

- Use ONLY the supplied study material.
- Do NOT invent facts.
- Questions must test understanding, application and analysis.
- Each question must contain between TWO and FIVE subquestions.
- Do NOT number the questions.
- Do NOT label the subquestions.
- Do NOT include marks.
- Do NOT include marking schemes.
- Do NOT include model answers.
- Do NOT include instructions.
- Do NOT include topic.
- Do NOT include difficulty.

Return ONLY valid JSON.

The JSON MUST follow this schema exactly:

{{
  "questions": [
    {{
      "question": "...",
      "subquestions": [
        "...",
        "...",
        "..."
      ]
    }}
  ]
}}

IMPORTANT

- Return ONLY JSON.
- No markdown.
- No code fences.
- No explanations.
- No text before JSON.
- No text after JSON.
"""
