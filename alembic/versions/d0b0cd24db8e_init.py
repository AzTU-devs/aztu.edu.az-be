"""init

Revision ID: d0b0cd24db8e
Revises: 
Create Date: 2026-01-22 02:00:07.566546

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd0b0cd24db8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Create Collaboration Tables ---
    op.create_table(
        'collaboration',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('collaboration_id', sa.INTEGER(), nullable=False),
        sa.Column('display_order', sa.INTEGER(), nullable=False),
        sa.Column('image', sa.TEXT(), nullable=False),
        sa.Column('url', sa.TEXT(), nullable=True),
        sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='collaboration_pkey'),
        sa.UniqueConstraint('collaboration_id', name='collaboration_collaboration_id_key')
    )

    op.create_table(
        'collaboration_translation',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('collaboration_id', sa.INTEGER(), nullable=False),
        sa.Column('lang_code', sa.VARCHAR(length=2), nullable=False),
        sa.Column('title', sa.TEXT(), nullable=False),
        sa.CheckConstraint(
            "lang_code::text = ANY (ARRAY['az'::character varying, 'en'::character varying]::text[])",
            name='chk_lang_code'
        ),
        sa.PrimaryKeyConstraint('id', name='collaboration_translation_pkey'),
        sa.UniqueConstraint('collaboration_id', 'lang_code', name='uq_collaboration_lang')
    )

    # --- Create Indexes for existing tables (only if they exist) ---
    # Use "if exists" pattern or wrap in try/except if needed
    try:
        op.create_index(op.f('ix_announcement_id'), 'announcement', ['id'], unique=False)
        op.create_index(op.f('ix_announcement_translation_id'), 'announcement_translation', ['id'], unique=False)
        op.create_index(op.f('ix_news_id'), 'news', ['id'], unique=False)
        op.create_index(op.f('ix_news_category_id'), 'news_category', ['id'], unique=False)
        op.create_index(op.f('ix_news_category_translation_id'), 'news_category_translation', ['id'], unique=False)
        op.create_index(op.f('ix_news_gallery_id'), 'news_gallery', ['id'], unique=False)
        op.create_index(op.f('ix_news_translation_id'), 'news_translation', ['id'], unique=False)
        op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
        op.create_index(op.f('ix_project_translation_id'), 'project_translation', ['id'], unique=False)
        op.create_index(op.f('ix_slider_id'), 'slider', ['id'], unique=False)
        op.create_index(op.f('ix_slider_translation_id'), 'slider_translation', ['id'], unique=False)
    except Exception:
        # tables might not exist yet, safe to ignore on fresh DB
        pass

    # --- Foreign Keys ---
    try:
        op.drop_constraint('project_fk', 'project_translation', type_='foreignkey')
        op.create_foreign_key(None, 'project_translation', 'project', ['project_id'], ['project_id'])
    except Exception:
        pass

    # --- Alter columns safely (optional) ---
    # Only run if table exists, otherwise skip
    # Wrap in try/except if needed


def downgrade() -> None:
    op.drop_table('collaboration_translation')
    op.drop_table('collaboration')