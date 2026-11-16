"""add_notes_table

Revision ID: 3e735025af3e
Revises: 
Create Date: 2026-11-11 20:48:25.843720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e735025af3e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the notes table for player observations."""
    op.create_table(
        'notes',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('content', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], name='notes_player_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='notes_pkey'),
    )


def downgrade() -> None:
    """Remove the notes table."""
    op.drop_table('notes')
