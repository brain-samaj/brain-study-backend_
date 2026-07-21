from __future__ import annotations

from PIL import Image
import pytesseract

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class ImageExtractor(BaseExtractor):

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".webp",
    }

    def supports(self, suffix: str) -> bool:
        return suffix in self.IMAGE_EXTENSIONS

    def extract(self, source) -> ExtractionResult:

        image = Image.open(source)

        text = pytesseract.image_to_string(image)

        return ExtractionResult(
            text=text.strip(),
            page_count=1,
            metadata={
                "type": "image",
            },
        )
