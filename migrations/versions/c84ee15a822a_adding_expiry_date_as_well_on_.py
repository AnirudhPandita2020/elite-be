"""Adding expiry date as well on certificate

Revision ID: c84ee15a822a
Revises: e7b01a295f87
Create Date: 2023-01-13 12:54:27.630796

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c84ee15a822a'
down_revision = 'e7b01a295f87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('certificates', sa.Column('validity_till', sa.DATE(), nullable=False))


def downgrade() -> None:
    op.drop_column('certificates', 'validity_till')
