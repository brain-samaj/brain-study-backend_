from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.modules.exams.exceptions import AutosaveError
from app.modules.exams.repository import ExamRepository
from app.modules.exams.utils import ExamFileUtils


class ExamAutosaveService:
    """
    Enterprise Exam Autosave Engine.

    Responsibilities
    ----------------
    - Save objective answers.
    - Save typed theory answers.
    - Rebuild final answer after OCR.
    - Maintain latest student state.

    The frontend can autosave frequently.

    The backend remains the source of truth.
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
    ) -> None:

        self._repository = repository


    async def autosave_objective(
        self,
        *,
        session_id: UUID,
        question_id: UUID,
        selected_option: str,
    ):

        try:

            answer = await self._repository.get_answer(
                session_id=session_id,
                question_id=question_id,
            )

            if answer is None:

                answer = await (
                    self._repository
                    .create_answer(
                        session_id=session_id,
                        question_id=question_id,
                    )
                )


            answer.selected_option = (
                selected_option.strip()
            )

            answer.updated_at = (
                datetime.now(
                    UTC,
                )
            )


            await self._repository.commit()

            return answer


        except Exception as exc:

            raise AutosaveError(
                str(exc)
            ) from exc



    async def autosave_theory(
        self,
        *,
        session_id: UUID,
        question_id: UUID,
        text_answer: str,
    ):

        try:

            answer = await self._repository.get_answer(
                session_id=session_id,
                question_id=question_id,
            )

            if answer is None:

                answer = await (
                    self._repository
                    .create_answer(
                        session_id=session_id,
                        question_id=question_id,
                    )
                )


            answer.text_answer = (
                text_answer.strip()
            )


            answer.final_answer = (
                ExamFileUtils.merge_answers(
                    typed_answer=(
                        answer.text_answer
                    ),
                    ocr_answer=(
                        answer.ocr_answer
                    ),
                )
            )


            answer.updated_at = (
                datetime.now(
                    UTC,
                )
            )


            await self._repository.commit()

            return answer


        except Exception as exc:

            raise AutosaveError(
                str(exc)
            ) from exc



    async def rebuild_final_answer(
        self,
        *,
        session_id: UUID,
        question_id: UUID,
    ):

        try:

            answer = await self._repository.get_answer(
                session_id=session_id,
                question_id=question_id,
            )

            if answer is None:

                raise AutosaveError(
                    "Answer not found."
                )


            attachments = (
                answer.attachments
            )


            ocr_parts = []


            for attachment in attachments:

                if attachment.ocr_text:

                    ocr_parts.append(
                        attachment.ocr_text
                    )


            answer.ocr_answer = (
                "\n\n".join(
                    ocr_parts
                )
            )


            answer.final_answer = (
                ExamFileUtils.merge_answers(
                    typed_answer=(
                        answer.text_answer
                    ),
                    ocr_answer=(
                        answer.ocr_answer
                    ),
                )
            )


            answer.updated_at = (
                datetime.now(
                    UTC,
                )
            )


            await self._repository.commit()

            return answer


        except Exception as exc:

            raise AutosaveError(
                str(exc)
            ) from exc
