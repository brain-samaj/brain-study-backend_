from __future__ import annotations

import re


class TextCleaner:
    """
    Production-grade text normalization.

    Responsibilities

    - Normalize whitespace
    - Remove duplicate blank lines
    - Normalize Unicode quotes/dashes
    - Remove page artefacts
    - Remove repeated headers/footers
    - Preserve educational content
    """

    _MULTISPACE = re.compile(r"[ \t]+")
    _MULTIBLANK = re.compile(r"\n{3,}")

    def clean(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        replacements = {
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "–": "-",
            "—": "-",
            "\u00A0": " ",
            "\t": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        cleaned_lines: list[str] = []

        previous = ""

        for line in text.split("\n"):

            line = self._MULTISPACE.sub(" ", line).strip()

            if not line:
                cleaned_lines.append("")
                continue

            lower = line.lower()

            if lower.startswith("page ") and len(line) < 20:
                continue

            if line == previous:
                continue

            previous = line

            cleaned_lines.append(line)

        text = "\n".join(cleaned_lines)

        text = self._MULTIBLANK.sub("\n\n", text)

        return text.strip()
