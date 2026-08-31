"""honorary doctors

Revision ID: d4e5f6a7b8c9
Revises: c2d3e4f5a6b7
Create Date: 2026-08-31 00:00:00.000000

Adds the honorary doctor roll so the list is editable from the admin dashboard
instead of being hardcoded in the website. Unbounded in size, ordered by
`display_order`, with one translation row per language.
"""
from alembic import op
import sqlalchemy as sa

revision = "d4e5f6a7b8c9"
down_revision = "c2d3e4f5a6b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "honorary_doctor",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_honorary_doctor_id"), "honorary_doctor", ["id"], unique=False)

    op.create_table(
        "honorary_doctor_tr",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("lang_code", sa.String(length=2), nullable=False),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["doctor_id"], ["honorary_doctor.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # One row per language per person.
        sa.UniqueConstraint("doctor_id", "lang_code", name="uq_honorary_doctor_tr_doctor_lang"),
    )
    op.create_index(op.f("ix_honorary_doctor_tr_id"), "honorary_doctor_tr", ["id"], unique=False)
    op.create_index(
        op.f("ix_honorary_doctor_tr_doctor_id"), "honorary_doctor_tr", ["doctor_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_honorary_doctor_tr_doctor_id"), table_name="honorary_doctor_tr")
    op.drop_index(op.f("ix_honorary_doctor_tr_id"), table_name="honorary_doctor_tr")
    op.drop_table("honorary_doctor_tr")
    op.drop_index(op.f("ix_honorary_doctor_id"), table_name="honorary_doctor")
    op.drop_table("honorary_doctor")
