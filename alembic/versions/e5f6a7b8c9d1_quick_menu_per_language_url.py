"""quick menu per-language url

Revision ID: e5f6a7b8c9d1
Revises: d4e5f6a7b8c9
Create Date: 2026-08-31 00:00:00.000000

The az and en sites use different paths for the same page, so a quick-menu link
has to be per language. Adds a nullable `url` to the two item translation tables;
NULL keeps falling back to the shared column on the parent row, so existing rows
keep working untouched.
"""
from alembic import op
import sqlalchemy as sa

revision = "e5f6a7b8c9d1"
down_revision = "d4e5f6a7b8c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "menu_quick_left_item_translations", sa.Column("url", sa.Text(), nullable=True)
    )
    op.add_column(
        "menu_quick_section_item_translations", sa.Column("url", sa.Text(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("menu_quick_section_item_translations", "url")
    op.drop_column("menu_quick_left_item_translations", "url")
