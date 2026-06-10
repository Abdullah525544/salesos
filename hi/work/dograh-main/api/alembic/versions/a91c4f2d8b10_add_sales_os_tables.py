"""add sales os tables

Revision ID: a91c4f2d8b10
Revises: 384be6596b36
Create Date: 2026-06-04 02:10:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a91c4f2d8b10"
down_revision: Union[str, None] = "384be6596b36"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sales_companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=64), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("google_rating", sa.Float(), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "name", "website", name="uq_sales_companies_org_name_website"),
    )
    op.create_index("ix_sales_companies_org_location", "sales_companies", ["organization_id", "country", "city"])
    op.create_index("ix_sales_companies_org_name", "sales_companies", ["organization_id", "name"])

    op.create_table(
        "sales_pipeline_stages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("is_closed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_won", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "key", name="uq_sales_pipeline_stage_org_key"),
    )
    op.create_index("ix_sales_pipeline_stages_org_position", "sales_pipeline_stages", ["organization_id", "position"])

    op.create_table(
        "sales_leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("business_name", sa.String(length=255), nullable=False),
        sa.Column("contact_name", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("niche", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("keyword", sa.String(length=255), nullable=True),
        sa.Column("google_rating", sa.Float(), nullable=True),
        sa.Column("lead_source", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("pipeline_stage", sa.String(length=64), nullable=False),
        sa.Column("quality_score", sa.Integer(), nullable=True),
        sa.Column("qualification_score", sa.Integer(), nullable=True),
        sa.Column("classification", sa.String(length=32), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=True),
        sa.Column("enrichment_status", sa.String(length=32), nullable=False),
        sa.Column("research_status", sa.String(length=32), nullable=False),
        sa.Column("next_action", sa.String(length=64), nullable=True),
        sa.Column("last_contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["sales_companies.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    for name, cols in {
        "ix_sales_leads_email": ["email"],
        "ix_sales_leads_phone": ["phone_number"],
        "ix_sales_leads_org_location": ["organization_id", "country", "city"],
        "ix_sales_leads_org_niche": ["organization_id", "niche"],
        "ix_sales_leads_org_stage": ["organization_id", "pipeline_stage"],
        "ix_sales_leads_org_status": ["organization_id", "status"],
    }.items():
        op.create_index(name, "sales_leads", cols)

    op.create_table(
        "sales_contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=64), nullable=True),
        sa.Column("social_url", sa.String(length=500), nullable=True),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["sales_companies.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_contacts_email", "sales_contacts", ["email"])
    op.create_index("ix_sales_contacts_org_lead", "sales_contacts", ["organization_id", "lead_id"])

    op.create_table(
        "sales_campaign_leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("attempt_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("campaign_id", "lead_id", name="uq_sales_campaign_leads_campaign_lead"),
    )
    op.create_index("ix_sales_campaign_leads_next_attempt", "sales_campaign_leads", ["next_attempt_at"])
    op.create_index("ix_sales_campaign_leads_org_state", "sales_campaign_leads", ["organization_id", "state"])

    op.create_table(
        "sales_calls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("campaign_id", sa.Integer(), nullable=True),
        sa.Column("workflow_run_id", sa.Integer(), nullable=True),
        sa.Column("external_call_id", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=64), nullable=True),
        sa.Column("direction", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("recording_url", sa.String(length=1000), nullable=True),
        sa.Column("cost_info", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_calls_campaign", "sales_calls", ["campaign_id"])
    op.create_index("ix_sales_calls_lead", "sales_calls", ["lead_id"])
    op.create_index("ix_sales_calls_org_created", "sales_calls", ["organization_id", "created_at"])
    op.create_index("ix_sales_calls_workflow_run", "sales_calls", ["workflow_run_id"])

    op.create_table(
        "sales_call_transcripts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("call_id", sa.Integer(), nullable=False),
        sa.Column("transcript_text", sa.Text(), nullable=False),
        sa.Column("segments", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("language", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["call_id"], ["sales_calls.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("call_id", name="uq_sales_call_transcripts_call"),
    )
    op.create_index("ix_sales_call_transcripts_org", "sales_call_transcripts", ["organization_id"])

    op.create_table(
        "sales_call_insights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("call_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("sentiment", sa.String(length=32), nullable=True),
        sa.Column("buying_signals", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("objections", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("qualification", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("qualification_score", sa.Integer(), nullable=True),
        sa.Column("recommended_next_action", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["call_id"], ["sales_calls.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("call_id", name="uq_sales_call_insights_call"),
    )
    op.create_index("ix_sales_call_insights_org_score", "sales_call_insights", ["organization_id", "qualification_score"])

    op.create_table(
        "sales_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.String(length=255), nullable=True),
        sa.Column("activity_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_activities_org_lead_created", "sales_activities", ["organization_id", "lead_id", "created_at"])

    op.create_table(
        "sales_meetings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("call_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("meeting_url", sa.String(length=1000), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["call_id"], ["sales_calls.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_meetings_lead", "sales_meetings", ["lead_id"])
    op.create_index("ix_sales_meetings_org_scheduled", "sales_meetings", ["organization_id", "scheduled_at"])

    op.create_table(
        "sales_follow_ups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("call_id", sa.Integer(), nullable=True),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["call_id"], ["sales_calls.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_followups_lead", "sales_follow_ups", ["lead_id"])
    op.create_index("ix_sales_followups_org_status_scheduled", "sales_follow_ups", ["organization_id", "status", "scheduled_at"])

    op.create_table(
        "sales_research_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("company_summary", sa.Text(), nullable=True),
        sa.Column("pain_points", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("opportunities", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("opening_lines", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("pitch_suggestions", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("sources", sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column("raw_report", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_by_agent", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["sales_companies.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_research_reports_created", "sales_research_reports", ["created_at"])
    op.create_index("ix_sales_research_reports_org_lead", "sales_research_reports", ["organization_id", "lead_id"])

    op.create_table(
        "sales_knowledge_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("knowledge_base_document_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("extra_metadata", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["knowledge_base_document_id"], ["knowledge_base_documents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_knowledge_sources_org_active", "sales_knowledge_sources", ["organization_id", "is_active"])
    op.create_index("ix_sales_knowledge_sources_org_category", "sales_knowledge_sources", ["organization_id", "category"])

    op.create_table(
        "sales_agent_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("agent_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("input", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("output", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("campaign_id", sa.Integer(), nullable=True),
        sa.Column("workflow_run_id", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["sales_leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sales_agent_runs_org_agent_created", "sales_agent_runs", ["organization_id", "agent_type", "created_at"])
    op.create_index("ix_sales_agent_runs_status", "sales_agent_runs", ["status"])


def downgrade() -> None:
    for table in (
        "sales_agent_runs",
        "sales_knowledge_sources",
        "sales_research_reports",
        "sales_follow_ups",
        "sales_meetings",
        "sales_activities",
        "sales_call_insights",
        "sales_call_transcripts",
        "sales_calls",
        "sales_campaign_leads",
        "sales_contacts",
        "sales_leads",
        "sales_pipeline_stages",
        "sales_companies",
    ):
        op.drop_table(table)
