from __future__ import annotations

import html
import re


class TextCleaner:
    """
    Cleans extracted text from PDF, DOCX, PPT,
    OCR images and manual topic descriptions.

    Every uploaded source passes through this class
    before chunking or embedding.
    """

    def clean(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        text = html.unescape(text)

        text = text.replace("\r", "\n")

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\s+([.,;:!?])",
            r"\1",
            text,
        )

        return text.strip()


    def normalize_unicode(
        self,
        text: str,
    ) -> str:

        return (
            text.encode(
                "utf-8",
                errors="ignore",
            )
            .decode(
                "utf-8",
            )
        )


    def prepare(
        self,
        text: str,
    ) -> str:

        text = self.normalize_unicode(
            text,
        )

        return self.clean(
            text,
        )
