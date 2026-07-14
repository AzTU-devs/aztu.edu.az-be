"""laboratory: add authorized_person contact field

Revision ID: b1c2d3e4f5a6
Revises: a7c91f3d2b48
Create Date: 2026-07-14

"""
from alembic import op
import sqlalchemy as sa


revision = 'b1c2d3e4f5a6'
down_revision = 'a7c91f3d2b48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cafedra_laboratories", sa.Column("authorized_person", sa.String(255)))


def downgrade() -> None:
    op.drop_column("cafedra_laboratories", "authorized_person")
