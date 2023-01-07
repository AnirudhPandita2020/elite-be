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
        sa.Column('road_tax', sa.String(), nullable=True),
        sa.Column('road_update_on', sa.DATE(), nullable=True),
        sa.Column('fitness_certificate', sa.String(), nullable=True),
        sa.Column('fitness_updated_on', sa.DATE(), nullable=True),
        sa.Column('goods_carrier_permission', sa.String(), nullable=True),
        sa.Column('goods_updated_on', sa.DATE(), nullable=True),
        sa.Column('national_permit', sa.String(), nullable=True),
        sa.Column('permit_updated_on', sa.DATE(), nullable=True),
        sa.Column('green_tax', sa.String(), nullable=True),
        sa.Column('green_tax_updated_on', sa.DATE(), nullable=True),
        sa.Column('insurance', sa.String(), nullable=True),
        sa.Column('insurance_updated_on', sa.DATE(), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('certificates')
