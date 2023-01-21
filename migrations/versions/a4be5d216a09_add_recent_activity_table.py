"""Add recent activity table

Revision ID: a4be5d216a09
Revises: c84ee15a822a
Create Date: 2023-01-15 20:34:04.611604

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a4be5d216a09'
down_revision = 'c84ee15a822a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('recent_activity',
                    sa.Column('activity_id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
                    sa.Column('activity_type', sa.String(), nullable=False),
                    sa.Column('work_on', sa.String(), nullable=False),
                    sa.Column('done_by', sa.String(), nullable=False),
                    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_table('recent_activity')
