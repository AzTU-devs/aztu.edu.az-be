"""news: add show_in_all_news flag

Revision ID: a7c91f3d2b48
Revises: e5f6a7b8c9d0
Create Date: 2026-05-26 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "a7c91f3d2b48"
down_revision = "e5f6a7b8c9d0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "news",
        sa.Column(
            "show_in_all_news",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column("news", "show_in_all_news")
