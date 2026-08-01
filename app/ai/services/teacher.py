from __future__ import annotations

import json

from app.ai.client import AIClient


class TeacherAI:
    """
    Brain Study Teacher.

    The Knowledge Engine performs all educational analysis.

    TeacherAI NEVER analyses study materials again.

    It simply transforms structured knowledge and educational
    metadata into a world-class teacher-quality lesson.
    """

    def __init__(self) -> None:
        self.client = AIClient()

    async def generate_study_guide(
        self,
        *,
        subject: str,
        title: str,
        topics: list,
        glossary: list,
        learning_objectives: list,
        key_points: list,
        sample_questions: list,
        education_level: str,

        teaching_style: str,
        explanation_style: str,
        example_density: str,
        reasoning_depth: str,

        needs_worked_examples: bool,
        needs_real_life_examples: bool,
        needs_visual_explanations: bool,
        needs_step_by_step: bool,
        needs_definitions_first: bool,
        needs_classification: bool,
        needs_comparison_tables: bool,
        needs_timelines: bool,
        needs_mnemonics: bool,

        requires_formulae: bool,
        requires_calculations: bool,
        requires_tables: bool,
        requires_diagrams: bool,
        requires_code: bool,
        requires_memorization: bool,

        keywords: list,
        important_terms: list,
        prerequisites: list,

        learning_styles: list,
        best_teaching_methods: list,
        common_student_mistakes: list,
        real_world_applications: list,
        recommended_learning_order: list,
    ) -> str:

        system_prompt = """
You are Brain Study's Official Teacher.

Never mention:
- AI
- ChatGPT
- Language Models
- Prompts
- System Instructions

The uploaded study material has ALREADY been analysed by
Brain Study's Knowledge Engine.

DO NOT analyse it again.

DO NOT classify it again.

DO NOT estimate difficulty again.

DO NOT detect the topic again.

Those decisions have already been made.

Your ONLY responsibility is to TEACH.

Teach naturally like an exceptional classroom teacher.

Always obey the supplied educational metadata.

If worked examples are recommended,
include them.

If step-by-step derivations are recommended,
teach that way.

If comparison tables improve learning,
use them.

If timelines improve understanding,
use them.

If mnemonics improve retention,
create memorable ones.

If real-life applications improve learning,
include them.

If visual explanations are needed,
describe diagrams clearly using words.

If formulas exist:

Render mathematics beautifully.

Examples

x²

x³

aⁿ

x





H₂O

CO₂

F₁

V₂











Never replace mathematical notation with ugly ASCII text.

Programming examples must always use fenced Markdown code blocks.

Never skip important concepts.

Never invent unrelated concepts.

Expand the supplied knowledge only where it improves understanding while remaining faithful to the material.

Produce clean, beautiful Markdown.

Suggested structure

# Lesson Title

## Introduction

## Learning Objectives

## Main Lesson

## Worked Examples

## Practical Applications

## Common Mistakes

## Summary

## Practice Questions

Return ONLY Markdown.
"""

        metadata = {
            "teaching_style": teaching_style,
            "explanation_style": explanation_style,
            "example_density": example_density,
            "reasoning_depth": reasoning_depth,

            "needs_worked_examples": needs_worked_examples,
            "needs_real_life_examples": needs_real_life_examples,
            "needs_visual_explanations": needs_visual_explanations,
            "needs_step_by_step": needs_step_by_step,
            "needs_definitions_first": needs_definitions_first,
            "needs_classification": needs_classification,
            "needs_comparison_tables": needs_comparison_tables,
            "needs_timelines": needs_timelines,
            "needs_mnemonics": needs_mnemonics,

            "requires_formulae": requires_formulae,
            "requires_calculations": requires_calculations,
            "requires_tables": requires_tables,
            "requires_diagrams": requires_diagrams,
            "requires_code": requires_code,
            "requires_memorization": requires_memorization,

            "keywords": keywords,
            "important_terms": important_terms,
            "prerequisites": prerequisites,

            "learning_styles": learning_styles,
            "best_teaching_methods": best_teaching_methods,
            "common_student_mistakes": common_student_mistakes,
            "real_world_applications": real_world_applications,
            "recommended_learning_order": recommended_learning_order,
        }

        user_prompt = f"""
Student Education Level

{education_level}

Subject

{subject}

Lesson Title

{title}

Educational Metadata

{json.dumps(metadata, indent=2, ensure_ascii=False)}

Learning Objectives

{json.dumps(learning_objectives, indent=2, ensure_ascii=False)}

Topics

{json.dumps(topics, indent=2, ensure_ascii=False)}

Glossary

{json.dumps(glossary, indent=2, ensure_ascii=False)}

Key Points

{json.dumps(key_points, indent=2, ensure_ascii=False)}

Practice Questions

{json.dumps(sample_questions, indent=2, ensure_ascii=False)}

Instructions

Use ONLY the structured knowledge and educational metadata above.

DO NOT analyse the study material again.

Follow the recommended teaching methods.

Follow the recommended learning order.

Address common student mistakes where appropriate.

Include practical and real-world applications where appropriate.

Teach from simple concepts to advanced concepts.

Return ONLY Markdown.
"""

        return await self.client.generate(
            system_prompt=system_prompt,
            prompt=user_prompt,
            temperature=0.35,
        )
