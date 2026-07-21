from __future__ import annotations

from pathlib import Path

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class TopicExtractor(BaseExtractor):

    def supports(self, suffix: str) -> bool:
        return suffix == ".topic"

    def extract(self, source: Path) -> ExtractionResult:
        return ExtractionResult(
            text=source.read_text(
                encoding="utf-8",
            ).strip(),
            page_count=1,
            metadata={
                "type": "topic"
            },
        )
