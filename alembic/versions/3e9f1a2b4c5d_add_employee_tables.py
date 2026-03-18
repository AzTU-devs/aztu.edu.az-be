"""add employee tables

Revision ID: 3e9f1a2b4c5d
Revises: 2a8d67c2d1a1
Create Date: 2026-03-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3e9f1a2b4c5d'
down_revision = '2a8d67c2d1a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Enums ────────────────────────────────────────────────────────────────
    day_of_week_enum = postgresql.ENUM(
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
        name='day_of_week_enum',
        create_type=True,
    )
    degree_level_enum = postgresql.ENUM(
        'Bachelor', 'Master', 'PhD',
        name='degree_level_enum',
        create_type=True,
    )
    education_level_enum = postgresql.ENUM(
        'bachelor', 'master',
        name='education_level_enum',
        create_type=True,
    )
    day_of_week_enum.create(op.get_bind(), checkfirst=True)
    degree_level_enum.create(op.get_bind(), checkfirst=True)
    education_level_enum.create(op.get_bind(), checkfirst=True)

    # ── employees ────────────────────────────────────────────────────────────
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('profile_image', sa.String(length=255), nullable=True),
        sa.Column('academic_degree', sa.String(length=100), nullable=True),
        sa.Column('academic_title', sa.String(length=100), nullable=True),
        sa.Column('position', sa.String(length=255), nullable=True),
        sa.Column('faculty_code', sa.String(length=50), nullable=True),
        sa.Column('cafedra_code', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('building', sa.String(length=100), nullable=True),
        sa.Column('floor', sa.String(length=20), nullable=True),
        sa.Column('room', sa.String(length=50), nullable=True),
        sa.Column('scopus_url', sa.Text(), nullable=True),
        sa.Column('google_scholar_url', sa.Text(), nullable=True),
        sa.Column('orcid_url', sa.Text(), nullable=True),
        sa.Column('researchgate_url', sa.Text(), nullable=True),
        sa.Column('academia_url', sa.Text(), nullable=True),
        sa.Column('scientific_interests', sa.Text(), nullable=True),
        sa.Column('publications', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['faculty_code'], ['faculties.faculty_code'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['cafedra_code'], ['cafedras.cafedra_code'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code'),
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)

    # ── employee_tr ──────────────────────────────────────────────────────────
    op.create_table(
        'employee_tr',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('lang_code', sa.String(length=10), nullable=False),
        sa.Column('biography', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code', 'lang_code', name='uq_employee_tr_code_lang'),
    )
    op.create_index(op.f('ix_employee_tr_id'), 'employee_tr', ['id'], unique=False)

    # ── office_hours ─────────────────────────────────────────────────────────
    op.create_table(
        'office_hours',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('day_of_week', sa.Enum(
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
            name='day_of_week_enum',
        ), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_office_hours_id'), 'office_hours', ['id'], unique=False)

    # ── education ────────────────────────────────────────────────────────────
    op.create_table(
        'education',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('degree_level', sa.Enum(
            'Bachelor', 'Master', 'PhD',
            name='degree_level_enum',
        ), nullable=False),
        sa.Column('institution', sa.String(length=255), nullable=False),
        sa.Column('specialization', sa.String(length=255), nullable=True),
        sa.Column('graduation_year', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_education_id'), 'education', ['id'], unique=False)

    # ── teaching_courses ─────────────────────────────────────────────────────
    op.create_table(
        'teaching_courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('course_name', sa.String(length=255), nullable=False),
        sa.Column('education_level', sa.Enum(
            'bachelor', 'master',
            name='education_level_enum',
        ), nullable=False),
        sa.ForeignKeyConstraint(['employee_code'], ['employees.employee_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_teaching_courses_id'), 'teaching_courses', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_teaching_courses_id'), table_name='teaching_courses')
    op.drop_table('teaching_courses')

    op.drop_index(op.f('ix_education_id'), table_name='education')
    op.drop_table('education')

    op.drop_index(op.f('ix_office_hours_id'), table_name='office_hours')
    op.drop_table('office_hours')

    op.drop_index(op.f('ix_employee_tr_id'), table_name='employee_tr')
    op.drop_table('employee_tr')

    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS day_of_week_enum")
    op.execute("DROP TYPE IF EXISTS degree_level_enum")
    op.execute("DROP TYPE IF EXISTS education_level_enum")
