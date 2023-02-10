"""type of certificate allowed

Revision ID: 67e2950cc819
Revises: d52a212832be
Create Date: 2023-01-25 13:46:17.639556

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '67e2950cc819'
down_revision = 'd52a212832be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('truck', sa.Column('certificate_disabled', sa.TEXT(), nullable=True))


def downgrade() -> None:
    op.drop_column('truck', 'certificate_disabled')
