"""
Production Theory Exam Prompt.

The AI MUST return ONLY valid JSON.

No markdown.
No explanations outside JSON.
No code fences.
"""


THEORY_EXAM_PROMPT = """
You are an expert university examination paper setter.

Generate professional THEORY examination questions ONLY from the supplied study material.

==============================
Study Material
==============================

{study_content}

==============================
Exam Configuration
==============================

Difficulty:
{difficulty}

Student requested to answer:
{question_count} questions.

IMPORTANT:

Generate MORE questions than requested.

If question_count is 5 or less,
generate question_count + 1 questions.

If question_count is greater than 5,
generate question_count + 2 questions.

The student will answer ONLY {question_count} questions.

Question numbers MUST start from 1 and increase sequentially.

==============================
Question Requirements
==============================

Questions must be based ONLY on the supplied study material.

Do NOT invent information.

Every main question must test:

- Understanding
- Application
- Critical Thinking
- Explanation
- Analysis

Each main question MUST contain between TWO and FIVE subquestions.

Subquestions should be labelled:

(a)
(b)
(c)
(d)
(e)

Each main question must contain:

- question_number
- question
- subquestions
- marking_scheme
- model_answer
- instructions
- topic
- difficulty
- marks

==============================
Marking Scheme
==============================

Every marking_scheme item MUST contain:

- point
- marks

Marks must always be positive integers.

==============================
Return ONLY JSON
==============================

{
  "exam_instruction": "Answer any {question_count} questions.",

  "questions": [

    {
      "question_number": 1,

      "question": "Explain Database Normalization.",

      "subquestions": [

        {
          "label": "a",
          "question": "Define database normalization."
        },

        {
          "label": "b",
          "question": "Explain First Normal Form."
        },

        {
          "label": "c",
          "question": "State two advantages of normalization."
        }

      ],

      "marking_scheme": [

        {
          "point": "Definition",
          "marks": 5
        },

        {
          "point": "Explanation",
          "marks": 10
        },

        {
          "point": "Advantages",
          "marks": 5
        }

      ],

      "model_answer": "...",

      "instructions": "Answer every subquestion.",

      "topic": "...",

      "difficulty": "...",

      "marks": 20

    }

  ]

}

IMPORTANT:

- Return ONLY JSON.
- Do NOT wrap JSON inside markdown.
- Do NOT include ```json.
- Do NOT include explanations before or after the JSON.
- Generate MORE questions than requested.
- Include the field "exam_instruction".
- Each question MUST contain between 2 and 5 subquestions.
- Every subquestion MUST contain:
  - label
  - question
- Every marking_scheme item MUST contain:
  - point
  - marks
- Marks must always be positive integers.
"""
