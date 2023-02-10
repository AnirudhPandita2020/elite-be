"""creating notification token table

Revision ID: d52a212832be
Revises: a4be5d216a09
Create Date: 2023-01-25 13:41:06.906231

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd52a212832be'
down_revision = 'a4be5d216a09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'notification_token',
        sa.Column("email_id", sa.String(), nullable=False, unique=True, primary_key=True),
        sa.Column("token", sa.TEXT(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('notification_token')
