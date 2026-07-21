from __future__ import annotations

from pptx import Presentation

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class PptxExtractor(BaseExtractor):

    def supports(self, suffix: str) -> bool:
        return suffix == ".pptx"

    def extract(self, source) -> ExtractionResult:

        presentation = Presentation(source)

        slides: list[str] = []

        for slide in presentation.slides:

            for shape in slide.shapes:

                if hasattr(shape, "text"):

                    text = shape.text.strip()

                    if text:
                        slides.append(text)

        return ExtractionResult(
            text="\n".join(slides),
            page_count=len(presentation.slides),
            metadata={
                "type": "pptx",
            },
        )
