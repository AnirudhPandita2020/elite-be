"""add active column for truck

Revision ID: 5b10440b9692
Revises: e7c51ef4d28d
Create Date: 2023-01-30 15:47:47.810723

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5b10440b9692'
down_revision = 'e7c51ef4d28d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('truck', sa.Column('is_active', sa.Boolean(), server_default='True'))


def downgrade() -> None:
    op.drop_column('truck', 'is_active')
