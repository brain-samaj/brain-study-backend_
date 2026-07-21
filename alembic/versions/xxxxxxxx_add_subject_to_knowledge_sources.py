"""add subject to knowledge_sources

Revision ID: xxxxxxxx
Revises: 43d856437cef
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "xxxxxxxx"
down_revision = "43d856437cef"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "knowledge_sources",
        sa.Column(
            "subject",
            sa.String(length=120),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE knowledge_sources SET subject='General' WHERE subject IS NULL"
    )

    op.alter_column(
        "knowledge_sources",
        "subject",
        nullable=False,
    )

    op.create_index(
        "ix_knowledge_subject",
        "knowledge_sources",
        ["subject"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_knowledge_subject",
        table_name="knowledge_sources",
    )

    op.drop_column(
        "knowledge_sources",
        "subject",
    )
