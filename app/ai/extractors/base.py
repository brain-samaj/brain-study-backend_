from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ExtractionResult:
    text: str
    page_count: int | None = None
    metadata: dict | None = None


class BaseExtractor(ABC):

    @abstractmethod
    def supports(self, suffix: str) -> bool:
        ...

    @abstractmethod
    def extract(self, source: Path) -> ExtractionResult:
        ...
