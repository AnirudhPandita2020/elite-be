"""truck_model

Revision ID: b0fb82d29572
Revises: 44ca2e1c5cde
Create Date: 2023-01-07 18:54:56.617311

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b0fb82d29572'
down_revision = '44ca2e1c5cde'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "truck",
        sa.Column('truck_id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('site', sa.String(), nullable=False),
        sa.Column('trailer_number', sa.String(), nullable=False, unique=True),
        sa.Column('trailer_info', sa.String(), nullable=False),
        sa.Column('chasis_number', sa.String(), unique=True, nullable=False),
        sa.Column('engine_number', sa.String(), nullable=False),
        sa.Column('trailer_length', sa.String(), nullable=False),
        sa.Column('suspension', sa.String(), nullable=False),
        sa.Column('created_on', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('truck')
