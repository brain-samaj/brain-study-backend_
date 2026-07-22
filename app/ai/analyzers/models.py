from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentAnalysis:
    """
    Structured analysis describing a study document.

    This drives every learning feature inside Brain Study.
    """

    title: str

    subject: str

    topic: str

    difficulty: str

    language: str

    education_level: str

    estimated_reading_minutes: int

    word_count: int

    requires_calculations: bool = False

    requires_formulae: bool = False

    requires_tables: bool = False

    requires_diagrams: bool = False

    requires_code: bool = False

    requires_memorization: bool = False

    keywords: list[str] = field(default_factory=list)

    learning_objectives: list[str] = field(default_factory=list)

    important_terms: list[str] = field(default_factory=list)

    prerequisites: list[str] = field(default_factory=list)

    learning_style: str = "mixed"

    confidence: float = 0.0
