"""laboratory: add bilingual equipments (names) tables

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-07-14

"""
from alembic import op
import sqlalchemy as sa


revision = 'c2d3e4f5a6b7'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cafedra_laboratory_equipments",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("laboratory_id", sa.Integer(), sa.ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_laboratory_equipment_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("equipment_id", sa.Integer(), sa.ForeignKey("cafedra_laboratory_equipments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("equipment_id", "lang_code", name="uq_cafedra_lab_equipment_tr_id_lang"),
    )


def downgrade() -> None:
    op.drop_table("cafedra_laboratory_equipment_tr")
    op.drop_table("cafedra_laboratory_equipments")
