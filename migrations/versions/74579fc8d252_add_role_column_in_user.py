"""Add role column in user

Revision ID: 74579fc8d252
Revises: a5fe7776ce8f
Create Date: 2023-02-06 19:52:19.113544

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '74579fc8d252'
down_revision = 'a5fe7776ce8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'role')
