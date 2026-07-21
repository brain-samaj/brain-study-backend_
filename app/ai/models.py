from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


############################################################
#
# BLOCK TYPES
#
############################################################

class BlockType(str, Enum):

    HEADING = "heading"

    PARAGRAPH = "paragraph"

    EQUATION = "equation"

    EXAMPLE = "example"

    NOTE = "note"

    WARNING = "warning"

    TABLE = "table"

    CODE = "code"

    DIAGRAM = "diagram"

    LIST = "list"

    IMAGE = "image"

    FLASHCARD = "flashcard"

    QUESTION = "question"


############################################################
#
# CONTENT BLOCK
#
############################################################

class ContentBlock(BaseModel):

    type: BlockType

    title: str | None = None

    content: str | None = None

    latex: str | None = None

    language: str | None = None

    table: dict | None = None

    items: list[str] | None = None

    metadata: dict | None = None


############################################################
#
# DOCUMENT
#
############################################################

class LearningDocument(BaseModel):

    title: str

    subject: str

    topic: str

    blocks: list[ContentBlock]
