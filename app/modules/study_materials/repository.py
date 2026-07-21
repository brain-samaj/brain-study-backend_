from __future__ import annotations

from uuid import UUID

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.study_materials.models import StudyMaterial


class StudyMaterialRepository:
    """
    Repository responsible for all persistence operations
    related to study materials.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        material: StudyMaterial,
    ) -> StudyMaterial:
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def get_by_id(
        self,
        material_id: UUID,
    ) -> StudyMaterial | None:
        stmt = (
            select(StudyMaterial)
            .where(
                StudyMaterial.id == material_id,
                StudyMaterial.deleted_at.is_(None),
            )
        )
        return self.db.scalar(stmt)

    def get_by_user(
        self,
        material_id: UUID,
        user_id: UUID,
    ) -> StudyMaterial | None:
        stmt = (
            select(StudyMaterial)
            .where(
                StudyMaterial.id == material_id,
                StudyMaterial.user_id == user_id,
                StudyMaterial.deleted_at.is_(None),
            )
        )
        return self.db.scalar(stmt)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[StudyMaterial]:
        stmt = (
            select(StudyMaterial)
            .where(
                StudyMaterial.user_id == user_id,
                StudyMaterial.deleted_at.is_(None),
            )
            .order_by(StudyMaterial.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def count_by_user(
        self,
        user_id: UUID,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(StudyMaterial)
            .where(
                StudyMaterial.user_id == user_id,
                StudyMaterial.deleted_at.is_(None),
            )
        )

        return int(self.db.scalar(stmt) or 0)

    def update(
        self,
        material: StudyMaterial,
    ) -> StudyMaterial:
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def delete(
        self,
        material: StudyMaterial,
    ) -> None:
        self.db.delete(material)
        self.db.commit()

    def soft_delete(
        self,
        material: StudyMaterial,
    ) -> StudyMaterial:
        material.deleted_at = func.now()

        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)

        return material

    def exists(
        self,
        material_id: UUID,
    ) -> bool:
        stmt = (
            select(StudyMaterial.id)
            .where(
                StudyMaterial.id == material_id,
                StudyMaterial.deleted_at.is_(None),
            )
        )

        return self.db.scalar(stmt) is not None
