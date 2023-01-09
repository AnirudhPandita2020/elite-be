"""certificate_model

Revision ID: 3e90e095dae3
Revises: b0fb82d29572
Create Date: 2023-01-07 18:55:32.380482

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3e90e095dae3'
down_revision = 'b0fb82d29572'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "certificates",
        sa.Column('certificate_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('truck_id', sa.Integer(), sa.ForeignKey('truck.truck_id', ondelete="CASCADE"), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('certificate_link', sa.String(), nullable=False),
        sa.Column('updated_on', sa.DATE(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('certificates')
