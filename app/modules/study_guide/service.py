from app.ai.services.orchestrator import AIOrchestrator
from app.modules.knowledge_engine.repository import KnowledgeRepository


class StudyGuideService:

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository
        self.ai = AIOrchestrator()


    async def generate(
        self,
        knowledge_source_id,
        education_level,
    ):

        source = self.repository.get(
            knowledge_source_id,
        )

        return await self.ai.build_learning_pack(
            subject=source.subject,
            title=source.title,
            material=source.cleaned_text,
            education_level=education_level,
        )
