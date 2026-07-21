from __future__ import annotations

import json

from app.ai.client import AIClient
from app.ai.analyzers.models import DocumentAnalysis
from app.ai.prompts.document_analysis import DOCUMENT_ANALYSIS_PROMPT


class DocumentAnalyzer:

    def __init__(self) -> None:
        self.client = AIClient()

    def analyze(
        self,
        text: str,
    ) -> DocumentAnalysis:

        prompt = f"""
{DOCUMENT_ANALYSIS_PROMPT}

DOCUMENT

{text[:15000]}
"""

        response = self.client.chat(prompt)

        data = json.loads(response)

        return DocumentAnalysis.model_validate(data)
