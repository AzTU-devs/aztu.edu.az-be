"""cafedra: expand to match faculty structure

Revision ID: c4e8f2a7b9d3
Revises: bc19f37950a9
Create Date: 2026-04-10

"""
from alembic import op
import sqlalchemy as sa


revision = 'c4e8f2a7b9d3'
down_revision = 'bc19f37950a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Section tables (6 pairs = 12 tables) ---

    op.create_table(
        "cafedra_laboratories",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_laboratory_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("laboratory_id", sa.Integer(), sa.ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("laboratory_id", "lang_code", name="uq_cafedra_laboratory_tr_id_lang"),
    )

    op.create_table(
        "cafedra_research_works",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_research_work_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("research_work_id", sa.Integer(), sa.ForeignKey("cafedra_research_works.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("research_work_id", "lang_code", name="uq_cafedra_research_work_tr_id_lang"),
    )

    op.create_table(
        "cafedra_partner_companies",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_partner_company_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("partner_company_id", sa.Integer(), sa.ForeignKey("cafedra_partner_companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("partner_company_id", "lang_code", name="uq_cafedra_partner_company_tr_id_lang"),
    )

    op.create_table(
        "cafedra_objectives",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_objective_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("objective_id", sa.Integer(), sa.ForeignKey("cafedra_objectives.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("objective_id", "lang_code", name="uq_cafedra_objective_tr_id_lang"),
    )

    op.create_table(
        "cafedra_duties",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_duty_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("duty_id", sa.Integer(), sa.ForeignKey("cafedra_duties.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("duty_id", "lang_code", name="uq_cafedra_duty_tr_id_lang"),
    )

    op.create_table(
        "cafedra_projects",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_project_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("cafedra_projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("project_id", "lang_code", name="uq_cafedra_project_tr_id_lang"),
    )

    # --- Personnel tables (2 pairs = 4 tables) ---

    op.create_table(
        "cafedra_deputy_directors",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("father_name", sa.String(100)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("profile_image", sa.String(1024)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_deputy_director_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("deputy_director_id", sa.Integer(), sa.ForeignKey("cafedra_deputy_directors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("scientific_name", sa.String(255)),
        sa.Column("scientific_degree", sa.String(255)),
        sa.Column("duty", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("deputy_director_id", "lang_code", name="uq_cafedra_deputy_director_tr_id_lang"),
    )

    op.create_table(
        "cafedra_scientific_council",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cafedra_code", sa.String(50), sa.ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("father_name", sa.String(100)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_council_member_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("council_member_id", sa.Integer(), sa.ForeignKey("cafedra_scientific_council.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("duty", sa.String(255), nullable=False),
        sa.Column("scientific_name", sa.String(255)),
        sa.Column("scientific_degree", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("council_member_id", "lang_code", name="uq_cafedra_council_member_tr_id_lang"),
    )

    # --- Director scientific events (1 pair = 2 tables) ---

    op.create_table(
        "cafedra_director_scientific_events",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("director_id", sa.Integer(), sa.ForeignKey("cafedra_directors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "cafedra_director_scientific_event_tr",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("scientific_event_id", sa.Integer(), sa.ForeignKey("cafedra_director_scientific_events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lang_code", sa.String(10), nullable=False),
        sa.Column("event_title", sa.String(255), nullable=False),
        sa.Column("event_description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("scientific_event_id", "lang_code", name="uq_cafedra_director_scientific_event_tr_id_lang"),
    )


def downgrade() -> None:
    op.drop_table("cafedra_director_scientific_event_tr")
    op.drop_table("cafedra_director_scientific_events")
    op.drop_table("cafedra_council_member_tr")
    op.drop_table("cafedra_scientific_council")
    op.drop_table("cafedra_deputy_director_tr")
    op.drop_table("cafedra_deputy_directors")
    op.drop_table("cafedra_project_tr")
    op.drop_table("cafedra_projects")
    op.drop_table("cafedra_duty_tr")
    op.drop_table("cafedra_duties")
    op.drop_table("cafedra_objective_tr")
    op.drop_table("cafedra_objectives")
    op.drop_table("cafedra_partner_company_tr")
    op.drop_table("cafedra_partner_companies")
    op.drop_table("cafedra_research_work_tr")
    op.drop_table("cafedra_research_works")
    op.drop_table("cafedra_laboratory_tr")
    op.drop_table("cafedra_laboratories")
