from __future__ import annotations

import re
from typing import Any


class LatexFormatter:
    """
    Enterprise LaTeX formatter for Brain Study.

    Pipeline

    Payload
      ↓
    Recursive walk
      ↓
    Protect existing LaTeX
      ↓
    Format text
      ↓
    Restore LaTeX
      ↓
    Output
    """

    _PROTECTED = re.compile(
        r"(\$\$.*?\$\$|\$.*?\$|\\\\\(.*?\\\\\)|\\\\\[.*?\\\\\])",
        re.DOTALL,
    )

    def format_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Public entry point.
        """
        return self._walk(payload)

    # =====================================================
    # Recursive walker
    # =====================================================

    def _walk(
        self,
        value: Any,
    ) -> Any:

        if isinstance(value, dict):
            return {
                key: self._walk(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self._walk(item)
                for item in value
            ]

        if isinstance(value, str):
            return self._format_string(value)

        return value

    # =====================================================
    # String formatter
    # =====================================================

    def _format_string(
        self,
        text: str,
    ) -> str:

        if not text.strip():
            return text

        protected, placeholders = self._protect_existing(text)

        protected = self._normalize_whitespace(
            protected
        )

        protected = self._format_math(
            protected
        )

        protected = self._format_chemistry(
            protected
        )

        protected = self._format_equations(
            protected
        )

        protected = self._format_units(
            protected
        )

        protected = self._restore_existing(
            protected,
            placeholders,
        )

        return protected

    # =====================================================
    # Protection
    # =====================================================

    def _protect_existing(
        self,
        text: str,
    ) -> tuple[str, dict[str, str]]:

        placeholders: dict[str, str] = {}

        def replace(
            match: re.Match[str],
        ) -> str:

            key = (
                f"__LATEX_{len(placeholders)}__"
            )

            placeholders[key] = match.group(0)

            return key

        text = self._PROTECTED.sub(
            replace,
            text,
        )

        return text, placeholders

    def _restore_existing(
        self,
        text: str,
        placeholders: dict[str, str],
    ) -> str:

        for key, value in placeholders.items():
            text = text.replace(
                key,
                value,
            )

        return text

    # =====================================================
    # Helpers
    # =====================================================

    def _normalize_whitespace(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def _wrap_math(
        self,
        text: str,
    ) -> str:

        if not text:
            return text

        if text.startswith("$") and text.endswith("$"):
            return text

        return f"${text}$"

    # =====================================================
    # Domain formatters
    # =====================================================

    def _format_math(
        self,
        text: str,
    ) -> str:
        return text

    def _format_chemistry(
        self,
        text: str,
    ) -> str:
        return text

    def _format_equations(
        self,
        text: str,
    ) -> str:
        return text

    def _format_units(
        self,
        text: str,
    ) -> str:
        return text
