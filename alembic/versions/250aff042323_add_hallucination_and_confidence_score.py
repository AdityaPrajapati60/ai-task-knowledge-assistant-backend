"""add hallucination and confidence score"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '250aff042323'
down_revision = '3d32acd673b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'agent_runs',
        sa.Column('hallucination_score', sa.Float(), nullable=True)
    )
    op.add_column(
        'agent_runs',
        sa.Column('confidence_score', sa.Float(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('agent_runs', 'confidence_score')
    op.drop_column('agent_runs', 'hallucination_score')
