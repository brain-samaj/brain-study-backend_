from __future__ import annotations

from app.ai.analyzers.models import DocumentAnalysis


class StudyGuidePromptBuilder:

    @staticmethod
    def build(
        analysis: DocumentAnalysis,
        content: str,
    ) -> str:

        sections = [
            "Introduction",
            "Core Concepts",
            "Detailed Explanation",
            "Common Mistakes",
            "Practice Tips",
            "Exam Tips",
            "Conclusion",
        ]

        if analysis.requires_calculations:
            sections.extend([
                "Important Formulae",
                "Formula Explanation",
                "Worked Examples",
                "Step-by-Step Calculations",
                "Calculation Shortcuts",
            ])

        if analysis.requires_code:
            sections.extend([
                "Syntax",
                "Code Examples",
                "Output Explanation",
                "Debugging Tips",
                "Programming Best Practices",
            ])

        if analysis.requires_diagrams:
            sections.append("Diagram Explanation")

        if analysis.requires_tables:
            sections.append("Comparison Tables")

        if analysis.requires_memorization:
            sections.extend([
                "Memory Tricks",
                "Mnemonics",
            ])

        prompt = f"""
You are one of the world's best educators.

Create a COMPLETE study guide.

Subject:
{analysis.subject}

Topic:
{analysis.topic}

Difficulty:
{analysis.difficulty}

Learning Style:
{analysis.learning_style}

Sections Required:

{chr(10).join(f"- {s}" for s in sections)}

Rules

Teach from the uploaded material.

Do not summarize.

Explain every important idea.

Give practical examples.

Never skip difficult concepts.

Expand difficult concepts.

If formulas exist, explain every symbol.

If programming, explain every code line.

If history, include timelines.

If biology, explain processes.

If chemistry, explain reactions.

If mathematics, solve examples step-by-step.

Material

{content}
"""

        return prompt
