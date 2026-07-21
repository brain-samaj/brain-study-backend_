from enum import Enum


class SourceType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    TXT = "txt"
    IMAGE = "image"
    HANDWRITTEN = "handwritten"
    TOPIC = "topic"


class LearningStyle(str, Enum):
    THEORY = "theory"
    CALCULATION = "calculation"
    PROGRAMMING = "programming"
    MEDICAL = "medical"
    LEGISLATION = "legislation"
    MIXED = "mixed"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
