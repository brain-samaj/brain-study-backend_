from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.ai.extractors.image import ImageExtractor


class OCRService:
    """
    OCR service responsible for extracting text
    from uploaded handwritten or printed images.
    """

    def __init__(self):
        self.extractor = ImageExtractor()

    async def extract_text(
        self,
        *,
        image: UploadFile,
    ) -> str:

        suffix = Path(image.filename or "image.png").suffix.lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp:

            temp.write(await image.read())
            temp_path = temp.name

        result = self.extractor.extract(temp_path)

        Path(temp_path).unlink(missing_ok=True)

        return result.text
