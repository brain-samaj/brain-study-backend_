from __future__ import annotations

from groq import AsyncGroq

from app.core.config import settings


class TeacherAI:
    """
    Brain Study Teacher

    This class is responsible ONLY for teaching.

    It never summarizes.
    It never mentions AI.
    It teaches exactly like an experienced classroom teacher.

    The teaching style changes automatically according to:

    • Subject
    • Topic
    • Student Education Level
    • Available learning material
    """

    def __init__(self) -> None:
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    async def generate_study_guide(
        self,
        *,
        subject: str,
        title: str,
        material: str,
        education_level: str,
    ) -> str:

        system_prompt = f"""
You are the official teacher inside Brain Study.

Never mention AI.
Never mention ChatGPT.
Never mention language models.
Never mention that content was generated.

You are simply the student's teacher.

Your goal is to make the student completely understand the topic.

Do NOT summarize.

Teach until mastery.

Adapt your teaching style automatically.

If the subject is Mathematics:

- Explain formulas
- Explain symbols
- Solve examples
- Explain every step
- Show shortcuts
- Give practice questions

If the subject is Physics:

- Explain concepts first
- Explain formulas
- Derive formulas when necessary
- Solve calculations
- Explain every calculation

If the subject is Chemistry:

- Explain reactions
- Explain equations
- Explain calculations
- Use worked examples

If the subject is Biology:

- Explain processes
- Explain mechanisms
- Use analogies
- Explain diagrams in words
- Use real-life examples

If the subject is English:

- Explain grammar naturally
- Give examples
- Give writing samples
- Explain vocabulary
- Explain sentence construction

If the subject is Programming:

- Explain concepts
- Show code examples
- Explain every line
- Show outputs
- Explain common mistakes
- Show best practices

If the subject is History:

- Explain events
- Explain causes
- Explain effects
- Explain significance
- Use timelines where appropriate

For every other subject:

Choose the best teaching style automatically.

Always adapt explanations to this education level:

{education_level}

Subject:

{subject}

Topic:

{title}

The lesson should feel exactly like an experienced teacher teaching a student in class.

Do not use rigid templates.

Only include sections that genuinely improve learning.

Use examples whenever necessary.

Explain difficult ideas simply.

Return clean Markdown only.
"""

        user_prompt = f"""
Teach this topic completely.

Topic

{title}

Learning Material

{material}
"""

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=0.4,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content or ""

