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
            "Learning Objectives",
            "Core Concepts",
            "Detailed Explanation",
            "Worked Examples",
            "Practice Questions",
            "Common Mistakes",
            "Revision Summary",
            "Exam Tips",
            "Conclusion",
        ]

        if analysis.requires_calculations:
            sections.extend([
                "Important Formulae",
                "Formula Explanation",
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

        return f"""
You are an award-winning professor, textbook author and examination expert.

Your task is to produce a PROFESSIONAL STUDY GUIDE.

SUBJECT
{analysis.subject}

TOPIC
{analysis.topic}

DIFFICULTY
{analysis.difficulty}

LEARNING STYLE
{analysis.learning_style}

=========================
OUTPUT RULES
=========================

Return ONLY Markdown.

Use proper Markdown headings.

# Main Topic

## Sub Topic

### Sub Section

Separate every section with blank lines.

Use bullet lists whenever appropriate.

Use numbered lists for procedures.

Use markdown tables for comparisons.

Never write one huge paragraph.

=========================
MATHEMATICS
=========================

Whenever mathematics appears:

Write ALL mathematics using LaTeX.

Inline examples:

$x^2$

$a+b$

Display equations:

$$
x^2+5x+6=0
$$

Fractions:

$$
\\frac{{a}}{{b}}
$$

Square roots:

$$
\\sqrt{{x}}
$$

Exponents:

$$
x^2
$$

Subscripts:

$$
H_2O
$$

Matrices:

$$
\\begin{{bmatrix}}
1&2\\\\
3&4
\\end{{bmatrix}}
$$

Never use plain text like

x^2

1/2

sqrt(x)

Always use LaTeX.

=========================
TEACHING STYLE
=========================

Teach like a university lecturer.

Explain EVERY concept.

Define every important term.

Explain why.

Explain where it is used.

Give intuition.

Provide real-life applications.

After every major explanation provide at least one worked example.

Worked examples must be step-by-step.

Highlight important notes using Markdown blockquotes.

Example:

> Important Note

Highlight warnings.

Example:

> Exam Tip

Include shortcuts.

Include memory tricks.

Include common mistakes.

Include revision checkpoints.

Include practice questions.

=========================
VERY IMPORTANT
=========================

Do NOT summarize.

Do NOT skip difficult concepts.

Teach directly from the uploaded material.

Expand every concept clearly.

If formulas exist, explain every symbol.

If mathematics exists, solve examples step-by-step.

If chemistry exists, balance and explain reactions.

If programming exists, explain every line of code.

If history exists, include timelines.

If biology exists, explain every process.

=========================
REQUIRED SECTIONS
=========================

{chr(10).join(f"- {s}" for s in sections)}

=========================
SOURCE MATERIAL
=========================

{content}
"""
