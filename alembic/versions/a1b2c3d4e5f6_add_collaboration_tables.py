"""add collaboration tables

Revision ID: a1b2c3d4e5f6
Revises: 2a8d67c2d1a1
Create Date: 2026-03-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '2a8d67c2d1a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'collaboration',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('collaboration_id', sa.Integer(), nullable=False),
        sa.Column('logo', sa.Text(), nullable=False),
        sa.Column('website_url', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('collaboration_id', name='uq_collaboration_collaboration_id')
    )
    op.create_index(op.f('ix_collaboration_id'), 'collaboration', ['id'], unique=False)

    op.create_table(
        'collaboration_translation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('collaboration_id', sa.Integer(), nullable=False),
        sa.Column('lang_code', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['collaboration_id'], ['collaboration.collaboration_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('collaboration_id', 'lang_code', name='uq_collaboration_translation_id_lang')
    )
    op.create_index(op.f('ix_collaboration_translation_id'), 'collaboration_translation', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_collaboration_translation_id'), table_name='collaboration_translation')
    op.drop_table('collaboration_translation')
    op.drop_index(op.f('ix_collaboration_id'), table_name='collaboration')
    op.drop_table('collaboration')
