from __future__ import annotations


class ExamModuleException(Exception):
    """
    Base exception for Exam domain.
    """


# ============================================================
# Exam Lifecycle Exceptions
# ============================================================


class ExamNotFoundError(
    ExamModuleException,
):
    """
    Raised when an exam session does not exist.
    """



class ExamAlreadySubmittedError(
    ExamModuleException,
):
    """
    Raised when modifying a submitted exam.
    """



class ExamExpiredError(
    ExamModuleException,
):
    """
    Raised when exam duration has ended.
    """



class InvalidExamConfigurationError(
    ExamModuleException,
):
    """
    Raised for invalid exam settings.
    """



# ============================================================
# Answer Exceptions
# ============================================================


class InvalidAnswerError(
    ExamModuleException,
):
    """
    Raised when an answer is invalid.
    """



class AnswerNotFoundError(
    ExamModuleException,
):
    """
    Raised when an answer does not exist.
    """



class AutosaveError(
    ExamModuleException,
):
    """
    Raised when autosave fails.
    """



# ============================================================
# Submission Exceptions
# ============================================================


class SubmissionError(
    ExamModuleException,
):
    """
    Raised when exam submission fails.
    """



class DuplicateSubmissionError(
    ExamModuleException,
):
    """
    Raised when a duplicate submission occurs.
    """



# ============================================================
# AI Exceptions
# ============================================================


class ExamGenerationError(
    ExamModuleException,
):
    """
    Raised when AI exam generation fails.
    """



class ReviewGenerationError(
    ExamModuleException,
):
    """
    Raised when AI review generation fails.
    """



class TheoryGradingError(
    ExamModuleException,
):
    """
    Raised when AI theory grading fails.
    """



class ObjectiveGradingError(
    ExamModuleException,
):
    """
    Raised when objective grading fails.
    """



# ============================================================
# Attachment Exceptions
# ============================================================


class AttachmentError(
    ExamModuleException,
):
    """
    Raised for attachment processing failures.
    """



class InvalidAttachmentError(
    AttachmentError,
):
    """
    Raised for invalid uploaded files.
    """
