from uuid import UUID

from pydantic import BaseModel


class GenerateStudyGuideRequest(BaseModel):

    knowledge_source_id: UUID


class StudyGuideResponse(BaseModel):

    study_guide: dict
