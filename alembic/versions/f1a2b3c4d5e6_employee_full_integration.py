"""employee full integration

Revision ID: f1a2b3c4d5e6
Revises: 3e9f1a2b4c5d
Create Date: 2026-03-18 12:00:00.000000

Changes:
- Expand employee_tr with all translatable fields
- Create employee_contacts table
- Create employee_research table
- Create education_tr table
- Create teaching_course_tr table
- Remove duplicate flat columns from employees table
- Remove course_name from teaching_courses (moved to teaching_course_tr)
- Remove institution/specialization from education (moved to education_tr)
"""
from alembic import op
import sqlalchemy as sa

revision = 'f1a2b3c4d5e6'
down_revision = '3e9f1a2b4c5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Expand employee_tr ─────────────────────────────────────────────────
    op.add_column('employee_tr', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('employee_tr', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('employee_tr', sa.Column('full_name', sa.String(length=255), nullable=True))
    op.add_column('employee_tr', sa.Column('academic_degree', sa.String(length=100), nullable=True))
    op.add_column('employee_tr', sa.Column('academic_title', sa.String(length=100), nullable=True))
    op.add_column('employee_tr', sa.Column('position', sa.String(length=255), nullable=True))
    op.add_column('employee_tr', sa.Column('scientific_interests', sa.Text(), nullable=True))

    # ── 2. Create employee_contacts ───────────────────────────────────────────
    op.create_table(
        'employee_contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('building', sa.String(length=100), nullable=False),
        sa.Column('floor', sa.String(length=20), nullable=False),
        sa.Column('room', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code', name='uq_employee_contacts_code'),
    )
    op.create_index(op.f('ix_employee_contacts_id'), 'employee_contacts', ['id'], unique=False)

    # ── 3. Create employee_research ───────────────────────────────────────────
    op.create_table(
        'employee_research',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('scopus_url', sa.Text(), nullable=True),
        sa.Column('google_scholar_url', sa.Text(), nullable=True),
        sa.Column('orcid_url', sa.Text(), nullable=True),
        sa.Column('researchgate_url', sa.Text(), nullable=True),
        sa.Column('academia_url', sa.Text(), nullable=True),
        sa.Column('publications', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code', name='uq_employee_research_code'),
    )
    op.create_index(op.f('ix_employee_research_id'), 'employee_research', ['id'], unique=False)

    # ── 4. Create education_tr ────────────────────────────────────────────────
    op.create_table(
        'education_tr',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('education_id', sa.Integer(), nullable=False),
        sa.Column('lang_code', sa.String(length=10), nullable=False),
        sa.Column('institution', sa.String(length=255), nullable=True),
        sa.Column('specialization', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('education_id', 'lang_code', name='uq_education_tr_id_lang'),
    )
    op.create_index(op.f('ix_education_tr_id'), 'education_tr', ['id'], unique=False)

    # ── 5. Create teaching_course_tr ──────────────────────────────────────────
    op.create_table(
        'teaching_course_tr',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('lang_code', sa.String(length=10), nullable=False),
        sa.Column('course_name', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['teaching_courses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('course_id', 'lang_code', name='uq_teaching_course_tr_id_lang'),
    )
    op.create_index(op.f('ix_teaching_course_tr_id'), 'teaching_course_tr', ['id'], unique=False)

    # ── 6. Remove flat columns from employees ─────────────────────────────────
    op.drop_column('employees', 'first_name')
    op.drop_column('employees', 'last_name')
    op.drop_column('employees', 'full_name')
    op.drop_column('employees', 'academic_degree')
    op.drop_column('employees', 'academic_title')
    op.drop_column('employees', 'position')
    op.drop_column('employees', 'scientific_interests')
    op.drop_column('employees', 'publications')
    op.drop_column('employees', 'email')
    op.drop_column('employees', 'phone')
    op.drop_column('employees', 'building')
    op.drop_column('employees', 'floor')
    op.drop_column('employees', 'room')
    op.drop_column('employees', 'scopus_url')
    op.drop_column('employees', 'google_scholar_url')
    op.drop_column('employees', 'orcid_url')
    op.drop_column('employees', 'researchgate_url')
    op.drop_column('employees', 'academia_url')

    # ── 7. Remove old columns from education (now in education_tr) ────────────
    op.drop_column('education', 'institution')
    op.drop_column('education', 'specialization')

    # ── 8. Remove course_name from teaching_courses (now in teaching_course_tr)
    op.drop_column('teaching_courses', 'course_name')


def downgrade() -> None:
    # Restore teaching_courses.course_name
    op.add_column('teaching_courses', sa.Column('course_name', sa.String(length=255), nullable=True))

    # Restore education columns
    op.add_column('education', sa.Column('institution', sa.String(length=255), nullable=True))
    op.add_column('education', sa.Column('specialization', sa.String(length=255), nullable=True))

    # Restore employees flat columns
    op.add_column('employees', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('full_name', sa.String(length=255), nullable=True))
    op.add_column('employees', sa.Column('academic_degree', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('academic_title', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('position', sa.String(length=255), nullable=True))
    op.add_column('employees', sa.Column('scientific_interests', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('publications', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('email', sa.String(length=255), nullable=True))
    op.add_column('employees', sa.Column('phone', sa.String(length=50), nullable=True))
    op.add_column('employees', sa.Column('building', sa.String(length=100), nullable=True))
    op.add_column('employees', sa.Column('floor', sa.String(length=20), nullable=True))
    op.add_column('employees', sa.Column('room', sa.String(length=50), nullable=True))
    op.add_column('employees', sa.Column('scopus_url', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('google_scholar_url', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('orcid_url', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('researchgate_url', sa.Text(), nullable=True))
    op.add_column('employees', sa.Column('academia_url', sa.Text(), nullable=True))

    # Drop new tables
    op.drop_index(op.f('ix_teaching_course_tr_id'), table_name='teaching_course_tr')
    op.drop_table('teaching_course_tr')

    op.drop_index(op.f('ix_education_tr_id'), table_name='education_tr')
    op.drop_table('education_tr')

    op.drop_index(op.f('ix_employee_research_id'), table_name='employee_research')
    op.drop_table('employee_research')

    op.drop_index(op.f('ix_employee_contacts_id'), table_name='employee_contacts')
    op.drop_table('employee_contacts')

    # Remove employee_tr new columns
    op.drop_column('employee_tr', 'scientific_interests')
    op.drop_column('employee_tr', 'position')
    op.drop_column('employee_tr', 'academic_title')
    op.drop_column('employee_tr', 'academic_degree')
    op.drop_column('employee_tr', 'full_name')
    op.drop_column('employee_tr', 'last_name')
    op.drop_column('employee_tr', 'first_name')
