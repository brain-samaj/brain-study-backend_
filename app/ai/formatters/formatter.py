from __future__ import annotations

from typing import Any

from .math_formatter import MathFormatter


class Formatter:
    """
    Central Brain Study formatter.

    This is the ONLY formatter that application services should call.

    Pipeline:

        AI payload
            ↓
        recursive traversal
            ↓
        MathFormatter
            ↓
        final payload

    Non-string values are preserved unchanged.
    """

    def __init__(self) -> None:
        self.math = MathFormatter()

    def format_payload(self, value: Any) -> Any:
        """
        Recursively format every string in an AI payload.
        """
        return self._walk(value)

    def _walk(self, value: Any) -> Any:

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

    def _format_string(self, text: str) -> str:
        """
        Format a single piece of AI-generated text.

        MathFormatter is deliberately the first active
        domain formatter. Other domain formatters can be
        added here without changing application services.
        """

        if not text or not text.strip():
            return text

        return self.math.format(text)
