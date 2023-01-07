"""history_model

Revision ID: 7a0ab837b85a
Revises: 3e90e095dae3
Create Date: 2023-01-07 18:56:17.461591

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a0ab837b85a'
down_revision = '3e90e095dae3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "certificate_history",
        sa.Column('history_id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('certificate_type', sa.String(), nullable=False),
        sa.Column('certificate_link', sa.String(), nullable=False),
        sa.Column('truck_id', sa.Integer(), sa.ForeignKey('truck.truck_id', ondelete='CASCADE'), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('certificate_history')
