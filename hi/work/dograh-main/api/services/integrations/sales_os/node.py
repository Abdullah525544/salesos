from __future__ import annotations

from typing import Literal

from api.services.integrations.base import IntegrationNodeRegistration
from api.services.workflow.node_data import BaseNodeData
from api.services.workflow.node_specs._base import GraphConstraints, NodeCategory, PropertyType
from api.services.workflow.node_specs.model_spec import build_spec, node_spec, spec_field


def _registration(model: type[BaseNodeData], type_name: str) -> IntegrationNodeRegistration:
    return IntegrationNodeRegistration(
        type_name=type_name,
        data_model=model,
        node_spec=build_spec(model),
    )


@node_spec(
    name="sales_find_leads",
    display_name="Find Leads",
    description="Find businesses by niche, geography, keyword, and business category.",
    category=NodeCategory.integration,
    icon="Search",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "niche", "country", "city", "keyword", "category", "limit", "push_to_campaign_id"),
)
class FindLeadsNodeData(BaseNodeData):
    niche: str = spec_field(..., ui_type=PropertyType.string, description="Target niche, e.g. dentists or roofing companies.")
    country: str | None = spec_field(default=None, ui_type=PropertyType.string, description="Country to search.")
    city: str | None = spec_field(default=None, ui_type=PropertyType.string, description="City or region to search.")
    keyword: str | None = spec_field(default=None, ui_type=PropertyType.string, description="Search keyword.")
    category: str | None = spec_field(default=None, ui_type=PropertyType.string, description="Business category.")
    limit: int = spec_field(default=25, ge=1, le=250, ui_type=PropertyType.number, description="Maximum leads to return.")
    push_to_campaign_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Optional campaign ID to attach qualified leads to.")


@node_spec(
    name="sales_enrich_lead",
    display_name="Enrich Lead",
    description="Enrich a Sales OS lead with contact, website, address, and source data.",
    category=NodeCategory.integration,
    icon="Sparkles",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "required_fields"),
)
class EnrichLeadNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID. If omitted, the node reads lead_id from workflow context.")
    required_fields: str = spec_field(default="phone_number,website,email,address", ui_type=PropertyType.string, description="Comma-separated fields to enrich.")


@node_spec(
    name="sales_research_company",
    display_name="Research Company",
    description="Analyze company web and social sources before a sales call.",
    category=NodeCategory.integration,
    icon="FileSearch",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "include_social_profiles", "attach_to_lead"),
)
class ResearchCompanyNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID. If omitted, the node reads lead_id from workflow context.")
    include_social_profiles: bool = spec_field(default=True, ui_type=PropertyType.boolean, description="Include discovered social profiles in research.")
    attach_to_lead: bool = spec_field(default=True, ui_type=PropertyType.boolean, description="Attach the generated report to the lead record.")


@node_spec(
    name="sales_create_crm_lead",
    display_name="Create CRM Lead",
    description="Create a Sales OS CRM lead from workflow context variables.",
    category=NodeCategory.integration,
    icon="UserPlus",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "business_name_path", "phone_path", "email_path", "website_path", "stage"),
)
class CreateCRMLeadNodeData(BaseNodeData):
    business_name_path: str = spec_field(default="business_name", ui_type=PropertyType.string, description="Context key containing the business name.")
    phone_path: str = spec_field(default="phone_number", ui_type=PropertyType.string, description="Context key containing the phone number.")
    email_path: str = spec_field(default="email", ui_type=PropertyType.string, description="Context key containing the email.")
    website_path: str = spec_field(default="website", ui_type=PropertyType.string, description="Context key containing the website.")
    stage: str = spec_field(default="new_lead", ui_type=PropertyType.string, description="Initial pipeline stage.")


@node_spec(
    name="sales_launch_campaign",
    display_name="Launch Campaign",
    description="Attach leads to an existing Dograh campaign and mark them queued.",
    category=NodeCategory.integration,
    icon="Rocket",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "campaign_id", "lead_ids_context_key"),
)
class LaunchCampaignNodeData(BaseNodeData):
    campaign_id: int = spec_field(..., ui_type=PropertyType.number, description="Dograh campaign ID.")
    lead_ids_context_key: str = spec_field(default="lead_ids", ui_type=PropertyType.string, description="Context key containing Sales OS lead IDs.")


@node_spec(
    name="sales_start_call",
    display_name="Start Call",
    description="Start an outbound Dograh call for a Sales OS lead.",
    category=NodeCategory.integration,
    icon="PhoneCall",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "workflow_id", "telephony_configuration_id"),
)
class StartCallNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID.")
    workflow_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Dograh voice workflow ID.")
    telephony_configuration_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Outbound telephony configuration.")


@node_spec(
    name="sales_analyze_call",
    display_name="Analyze Call",
    description="Generate transcript summary, sentiment, objections, and buying signals.",
    category=NodeCategory.integration,
    icon="AudioLines",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "call_id", "store_transcript", "store_insights"),
)
class AnalyzeCallNodeData(BaseNodeData):
    call_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS call ID.")
    store_transcript: bool = spec_field(default=True, ui_type=PropertyType.boolean, description="Store transcript text.")
    store_insights: bool = spec_field(default=True, ui_type=PropertyType.boolean, description="Store generated call intelligence.")


@node_spec(
    name="sales_qualify_lead",
    display_name="Qualify Lead",
    description="Score a lead using interest, budget, need, authority, and timeline.",
    category=NodeCategory.integration,
    icon="Gauge",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "score_threshold_hot", "score_threshold_warm"),
)
class QualifyLeadNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID.")
    score_threshold_hot: int = spec_field(default=75, ge=0, le=100, ui_type=PropertyType.number, description="Minimum score for Hot Lead.")
    score_threshold_warm: int = spec_field(default=40, ge=0, le=100, ui_type=PropertyType.number, description="Minimum score for Warm Lead.")


@node_spec(
    name="sales_book_meeting",
    display_name="Book Meeting",
    description="Create a meeting record and move the lead to Meeting Scheduled.",
    category=NodeCategory.integration,
    icon="CalendarPlus",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "title", "duration_minutes", "meeting_url_context_key"),
)
class BookMeetingNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID.")
    title: str = spec_field(default="Sales consultation", ui_type=PropertyType.string, description="Meeting title.")
    duration_minutes: int = spec_field(default=30, ge=5, le=240, ui_type=PropertyType.number, description="Meeting duration.")
    meeting_url_context_key: str | None = spec_field(default="meeting_url", ui_type=PropertyType.string, description="Context key containing meeting URL.")


@node_spec(
    name="sales_update_pipeline",
    display_name="Update Pipeline",
    description="Update a Sales OS lead pipeline stage.",
    category=NodeCategory.integration,
    icon="Kanban",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "stage"),
)
class UpdatePipelineNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID.")
    stage: Literal["new_lead", "contacted", "interested", "meeting_scheduled", "proposal_sent", "closed_won", "closed_lost"] = spec_field(default="contacted", ui_type=PropertyType.options, description="Target pipeline stage.")


@node_spec(
    name="sales_schedule_follow_up",
    display_name="Schedule Follow-Up",
    description="Schedule a follow-up action for a Sales OS lead.",
    category=NodeCategory.integration,
    icon="Clock",
    graph_constraints=GraphConstraints(min_incoming=0, max_incoming=1, min_outgoing=0, max_outgoing=1),
    property_order=("name", "lead_id", "channel", "delay_minutes", "subject", "body"),
)
class ScheduleFollowUpNodeData(BaseNodeData):
    lead_id: int | None = spec_field(default=None, ui_type=PropertyType.number, description="Sales OS lead ID.")
    channel: Literal["email", "sms", "call", "task"] = spec_field(default="email", ui_type=PropertyType.options, description="Follow-up channel.")
    delay_minutes: int = spec_field(default=1440, ge=1, ui_type=PropertyType.number, description="Minutes from now to schedule follow-up.")
    subject: str | None = spec_field(default=None, ui_type=PropertyType.string, description="Follow-up subject.")
    body: str | None = spec_field(default=None, ui_type=PropertyType.mention_textarea, description="Follow-up body.")


NODES = (
    _registration(FindLeadsNodeData, "sales_find_leads"),
    _registration(EnrichLeadNodeData, "sales_enrich_lead"),
    _registration(ResearchCompanyNodeData, "sales_research_company"),
    _registration(CreateCRMLeadNodeData, "sales_create_crm_lead"),
    _registration(LaunchCampaignNodeData, "sales_launch_campaign"),
    _registration(StartCallNodeData, "sales_start_call"),
    _registration(AnalyzeCallNodeData, "sales_analyze_call"),
    _registration(QualifyLeadNodeData, "sales_qualify_lead"),
    _registration(BookMeetingNodeData, "sales_book_meeting"),
    _registration(UpdatePipelineNodeData, "sales_update_pipeline"),
    _registration(ScheduleFollowUpNodeData, "sales_schedule_follow_up"),
)
