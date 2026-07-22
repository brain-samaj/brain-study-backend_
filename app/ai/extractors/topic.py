from __future__ import annotations

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class TopicExtractor(BaseExtractor):
    SUPPORTED_EXTENSIONS = {".topic"}

    def supports(self, suffix: str) -> bool:
        return suffix.lower() in self.SUPPORTED_EXTENSIONS

    async def extract(
        self,
        *,
        title: str,
        subject: str,
        topic: str,
    ) -> ExtractionResult:
        """
        Extract text from a topic entered directly
        by the user instead of an uploaded file.
        """

        text = f"""Title: {title}

Subject: {subject}

{topic}
"""

        return ExtractionResult(
            text=text.strip(),
            page_count=1,
            metadata={
                "type": "topic",
                "title": title,
                "subject": subject,
            },
        )
