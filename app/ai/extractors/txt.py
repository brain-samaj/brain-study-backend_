from __future__ import annotations

from pathlib import Path

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class TxtExtractor(BaseExtractor):
    SUPPORTED_EXTENSIONS = {".txt"}

    def supports(self, suffix: str) -> bool:
        return suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract(
        self,
        source: Path,
    ) -> ExtractionResult:

        text = source.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return ExtractionResult(
            text=text.strip(),
            page_count=1,
            metadata={
                "type": "text",
            },
        )
