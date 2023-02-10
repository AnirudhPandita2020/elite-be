"""profile_photo

Revision ID: a5fe7776ce8f
Revises: 5b10440b9692
Create Date: 2023-02-05 18:45:44.065382

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a5fe7776ce8f'
down_revision = '5b10440b9692'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('profile_photo', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_table('users','profile_photo')
