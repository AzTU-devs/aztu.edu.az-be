"""cafedra relationships and constraints

Revision ID: 2a8d67c2d1a1
Revises: 6b3b3f0e2f2a
Create Date: 2026-01-25 15:28:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "2a8d67c2d1a1"
down_revision = "6b3b3f0e2f2a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_cafedras_code", "cafedras", ["cafedra_code"])
    op.create_foreign_key(
        "fk_cafedras_faculty_code",
        "cafedras",
        "faculties",
        ["faculty_code"],
        ["faculty_code"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "uq_cafedras_tr_code_lang",
        "cafedras_tr",
        ["cafedra_code", "lang_code"],
    )
    op.create_foreign_key(
        "fk_cafedras_tr_cafedra_code",
        "cafedras_tr",
        "cafedras",
        ["cafedra_code"],
        ["cafedra_code"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_cafedras_tr_cafedra_code", "cafedras_tr", type_="foreignkey")
    op.drop_constraint("uq_cafedras_tr_code_lang", "cafedras_tr", type_="unique")
    op.drop_constraint("fk_cafedras_faculty_code", "cafedras", type_="foreignkey")
    op.drop_constraint("uq_cafedras_code", "cafedras", type_="unique")
