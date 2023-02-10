"""add certificate name

Revision ID: e7c51ef4d28d
Revises: 67e2950cc819
Create Date: 2023-01-25 15:30:27.409844

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e7c51ef4d28d'
down_revision = '67e2950cc819'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('certificates', sa.Column('certificate_file_name', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('certificates', 'certificate_file_name')
