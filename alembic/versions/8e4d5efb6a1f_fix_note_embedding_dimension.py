"""fix note embedding dimension

Revision ID: 8e4d5efb6a1f
Revises: f1d2f4c3d7a9
Create Date: 2026-11-16 20:20:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8e4d5efb6a1f'
down_revision: Union[str, Sequence[str], None] = 'f1d2f4c3d7a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Update the pgvector dimension to match the Gemini embedding output."""
    op.execute('ALTER TABLE notes ALTER COLUMN embedding TYPE vector(3072)')


def downgrade() -> None:
    """Restore the legacy vector size if needed for rollback."""
    op.execute('ALTER TABLE notes ALTER COLUMN embedding TYPE vector(512)')
