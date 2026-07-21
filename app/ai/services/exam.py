from __future__ import annotations

from app.ai.services.document_extractor import DocumentExtractorService

from app.ai.exam_engine.objective_generator import ObjectiveExamGenerator
from app.ai.exam_engine.service import TheoryExamGenerator


class ExamService:

    def __init__(self):

        self.documents = DocumentExtractorService()

        self.theory = TheoryExamGenerator()

        self.objective = ObjectiveExamGenerator()

    def create_objective_exam(
        self,
        source: str,
        duration: int,
        questions: int,
    ):

        result = self.documents.process(source)

        paper = self.objective.generate(
            analysis=result["analysis"],
            material=result["extraction"].text,
            total_questions=questions,
        )

        paper.duration_minutes = duration

        return paper

    def create_theory_exam(
        self,
        source: str,
        duration: int,
        answer_any: int,
    ):

        result = self.documents.process(source)

        return self.theory.generate(
            analysis=result["analysis"],
            material=result["extraction"].text,
            duration=duration,
            answer_any=answer_any,
        )
EOFcat > app/ai/services/exam.py << 'EOF'
from __future__ import annotations

from app.ai.services.document_extractor import DocumentExtractorService

from app.ai.exam_engine.objective_generator import ObjectiveExamGenerator
from app.ai.exam_engine.service import TheoryExamGenerator


class ExamService:

    def __init__(self):

        self.documents = DocumentExtractorService()

        self.theory = TheoryExamGenerator()

        self.objective = ObjectiveExamGenerator()

    def create_objective_exam(
        self,
        source: str,
        duration: int,
        questions: int,
    ):

        result = self.documents.process(source)

        paper = self.objective.generate(
            analysis=result["analysis"],
            material=result["extraction"].text,
            total_questions=questions,
        )

        paper.duration_minutes = duration

        return paper

    def create_theory_exam(
        self,
        source: str,
        duration: int,
        answer_any: int,
    ):

        result = self.documents.process(source)

        return self.theory.generate(
            analysis=result["analysis"],
            material=result["extraction"].text,
            duration=duration,
            answer_any=answer_any,
        )
