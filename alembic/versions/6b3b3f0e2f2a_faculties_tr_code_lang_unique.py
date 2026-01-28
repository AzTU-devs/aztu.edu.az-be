"""faculties_tr composite unique

Revision ID: 6b3b3f0e2f2a
Revises: d0b0cd24db8e
Create Date: 2026-01-25 15:02:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "6b3b3f0e2f2a"
down_revision = "d0b0cd24db8e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("faculties_tr_facult_code_key", "faculties_tr", type_="unique")
    op.create_unique_constraint(
        "uq_faculties_tr_code_lang",
        "faculties_tr",
        ["facult_code", "lang_code"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_faculties_tr_code_lang", "faculties_tr", type_="unique")
    op.create_unique_constraint(
        "faculties_tr_facult_code_key",
        "faculties_tr",
        ["facult_code"],
    )
