"""add embedding to notes

Revision ID: f1d2f4c3d7a9
Revises: 3e735025af3e
Create Date: 2026-11-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = 'f1d2f4c3d7a9'
down_revision: Union[str, Sequence[str], None] = '3e735025af3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add embedding column to existing notes table without deleting data."""
    op.add_column('notes', sa.Column('embedding', Vector(512), nullable=True))


def downgrade() -> None:
    """Remove the embedding column from notes."""
    op.drop_column('notes', 'embedding')
