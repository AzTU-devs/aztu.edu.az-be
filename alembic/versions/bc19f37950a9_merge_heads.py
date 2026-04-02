"""merge heads

Revision ID: bc19f37950a9
Revises: a1b2c3d4e5f6, f1a2b3c4d5e6
Create Date: 2026-04-02 01:01:54.122834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc19f37950a9'
down_revision = ('a1b2c3d4e5f6', 'f1a2b3c4d5e6')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
