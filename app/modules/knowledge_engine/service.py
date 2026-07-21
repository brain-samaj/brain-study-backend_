from app.modules.knowledge_engine.repository import KnowledgeRepository


class KnowledgeEngineService:

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository


    async def create_topic(
        self,
        *,
        user_id,
        title,
        subject,
        topic_description,
    ):

        return self.repository.create_topic(
            user_id=user_id,
            title=title,
            subject=subject,
            topic_description=topic_description,
        )


    async def upload_document(
        self,
        *,
        user_id,
        file,
    ):

        return await self.repository.save_document(
            user_id=user_id,
            file=file,
        )
