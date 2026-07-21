from __future__ import annotations

import json
from dataclasses import dataclass

from app.ai.client import AIClient


@dataclass(slots=True)
class GeneratedExam:

    session: object

    questions: list


class ExamGenerator:

    def __init__(self):

        self.ai = AIClient()

    async def generate_exam(
        self,
        *,
        study_material,
        user,
        settings,
    ):

        material = study_material.extracted_text

        analysis = await self.analyse_material(
            material,
        )

        if settings.question_type == "objective":

            return await self.generate_objective_exam(
                material=material,
                analysis=analysis,
                settings=settings,
                user=user,
                study_material=study_material,
            )

        return await self.generate_theory_exam(
            material=material,
            analysis=analysis,
            settings=settings,
            user=user,
            study_material=study_material,
        )

    async def analyse_material(
        self,
        material: str,
    ):

        prompt = f"""
You are an expert university lecturer.

Analyse the uploaded study material.

Return ONLY JSON.

Determine

Subject

Main Topic

Sub Topics

Calculation Required

Needs Formula

Needs Worked Examples

Needs Diagram

Difficulty

Learning Style

JSON ONLY.

Material

{material[:25000]}
"""

        response = await self.ai.generate_json(
            prompt,
        )

        return json.loads(
            response,
        )

    async def generate_objective_exam(
        self,
        *,
        material: str,
        analysis: dict,
        settings,
        user,
        study_material,
    ):

        prompt = f"""
You are an experienced university examination board.

Generate a HIGH QUALITY university objective examination.

The questions MUST come ONLY from the uploaded material.

Never invent topics outside the material.

====================================

Subject

{analysis["Subject"]}

Main Topic

{analysis["Main Topic"]}

Sub Topics

{analysis["Sub Topics"]}

Difficulty

{analysis["Difficulty"]}

Calculation Required

{analysis["Calculation Required"]}

Needs Formula

{analysis["Needs Formula"]}

Needs Worked Examples

{analysis["Needs Worked Examples"]}

Needs Diagram

{analysis["Needs Diagram"]}

====================================

RULES

Generate exactly {settings.total_questions} questions.

Every question must have

A

B

C

D

One correct answer

Explanation

Difficulty

Topic

Marks

====================================

Randomisation

Every time this prompt runs:

• Use different concepts

• Shuffle options

• Change numerical values where applicable

• Use different scenarios

• Avoid repeating previous questions

• Preserve academic correctness

====================================

If the subject requires calculations

Generate computational questions.

If the subject requires formulas

Generate formula-based questions.

If diagrams are important

Describe the diagram clearly.

====================================

Return ONLY JSON.

Example

{{
    "questions":[
        {{
            "question":"",

            "options":{{

                "A":"",

                "B":"",

                "C":"",

                "D":""

            }},

            "answer":"A",

            "topic":"",

            "difficulty":"",

            "marks":1,

            "explanation":""
        }}
    ]
}}

Study Material

{material[:25000]}
"""

        response = await self.ai.generate_json(
            prompt,
        )

        questions = json.loads(response)["questions"]

        return self.build_objective_exam(
            questions=questions,
            settings=settings,
            user=user,
            study_material=study_material,
        )


    async def generate_theory_exam(
        self,
        *,
        material: str,
        analysis: dict,
        settings,
        user,
        study_material,
    ):

        total_questions = settings.total_questions

        if total_questions <= 5:
            questions_to_generate = total_questions + 2
        else:
            questions_to_generate = total_questions + 2

        prompt = f"""
You are a senior university lecturer.

Generate a REAL university examination paper.

The examination must look exactly like a real university exam.

==================================================

Subject

{analysis["Subject"]}

Main Topic

{analysis["Main Topic"]}

Sub Topics

{analysis["Sub Topics"]}

Difficulty

{analysis["Difficulty"]}

==================================================

The student requested

Answer {total_questions} Questions.

Generate

{questions_to_generate} Questions.

Instruction

Answer ANY {total_questions} Questions.

==================================================

Every question MUST contain

1(a)

1(b)

1(c)

1(d)

Each subsection must naturally continue from the previous one.

Do NOT generate unrelated subquestions.

==================================================

Every question MUST include

Mark Allocation

Complete Marking Scheme

Model Answer

Difficulty

Topic

Estimated Time

==================================================

If calculations are required

Generate proper university calculations.

Include

Worked Solution

Formula

Units

==================================================

If derivation is required

Generate derivation.

==================================================

If explanation is required

Generate explanation.

==================================================

If diagrams are required

Describe the diagram students should draw.

==================================================

Every time this exam is generated

Create NEW questions.

Never repeat previous exams.

==================================================

Return ONLY JSON.

Example

{{
    "instruction":"Answer ANY {total_questions} Questions.",

    "questions":[
        {{
            "number":1,

            "topic":"",

            "difficulty":"",

            "estimated_time":20,

            "total_marks":20,

            "question":{{
                "a":"",
                "b":"",
                "c":"",
                "d":""
            }},

            "marking_scheme":{{
                "a":[],
                "b":[],
                "c":[],
                "d":[]
            }},

            "model_answer":{{
                "a":"",
                "b":"",
                "c":"",
                "d":""
            }}
        }}
    ]
}}

Study Material

{material[:25000]}
"""

        response = await self.ai.generate_json(
            prompt,
        )

        data = json.loads(response)

        return self.build_theory_exam(
            questions=data["questions"],
            instruction=data["instruction"],
            settings=settings,
            user=user,
            study_material=study_material,
        )



