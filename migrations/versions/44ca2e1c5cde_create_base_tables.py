"""create_base_tables

Revision ID: 44ca2e1c5cde
Revises: 
Create Date: 2023-01-06 22:31:28.070739

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '44ca2e1c5cde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('authority_level', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), server_default='False'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table("users")
