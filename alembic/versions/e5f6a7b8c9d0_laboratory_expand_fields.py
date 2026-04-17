"""laboratory: add room_number, email, phone_number, objectives, gallery images

Revision ID: e5f6a7b8c9d0
Revises: c4e8f2a7b9d3
Create Date: 2026-04-17

"""
from alembic import op
import sqlalchemy as sa


revision = 'e5f6a7b8c9d0'
down_revision = 'c4e8f2a7b9d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to cafedra_laboratories
    op.add_column("cafedra_laboratories", sa.Column("room_number", sa.String(50)))
    op.add_column("cafedra_laboratories", sa.Column("email", sa.String(255)))
    op.add_column("cafedra_laboratories", sa.Column("phone_number", sa.String(50)))

    # Laboratory objectives
    op.create_table(
        "cafedra_laboratory_objectives",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("laboratory_id", sa.Integer(), sa.ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_laboratory_objective_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("objective_id", sa.Integer(), sa.ForeignKey("cafedra_laboratory_objectives.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("objective_id", "lang_code", name="uq_cafedra_lab_objective_tr_id_lang"),
    )

    # Laboratory gallery images
    op.create_table(
        "cafedra_laboratory_gallery_images",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("laboratory_id", sa.Integer(), sa.ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("image_url", sa.String(1024), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("cafedra_laboratory_gallery_images")
    op.drop_table("cafedra_laboratory_objective_tr")
    op.drop_table("cafedra_laboratory_objectives")
    op.drop_column("cafedra_laboratories", "phone_number")
    op.drop_column("cafedra_laboratories", "email")
    op.drop_column("cafedra_laboratories", "room_number")
