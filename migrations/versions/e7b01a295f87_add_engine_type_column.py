"""add engine type column

Revision ID: e7b01a295f87
Revises: 7a0ab837b85a
Create Date: 2023-01-07 19:03:15.592456

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e7b01a295f87'
down_revision = '7a0ab837b85a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('truck', sa.Column('engine', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('truck', 'engine')
