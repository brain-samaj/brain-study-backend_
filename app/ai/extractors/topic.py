from __future__ import annotations

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class TopicExtractor(BaseExtractor):

    SUPPORTED_EXTENSIONS = {".topic"}

    def supports(
        self,
        suffix: str,
    ) -> bool:
        return suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract(
        self,
        *,
        title: str,
        subject: str,
        topic: str,
    ) -> ExtractionResult:
        """
        Converts a manually entered topic into the
        same format used by uploaded documents.
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
