from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


PipelineStage = Literal[
    "new_lead",
    "contacted",
    "interested",
    "meeting_scheduled",
    "proposal_sent",
    "closed_won",
    "closed_lost",
]


class LeadFinderRequest(BaseModel):
    niche: str = Field(..., min_length=1, max_length=255)
    country: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    keyword: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=255)
    limit: int = Field(default=25, ge=1, le=250)


class SalesLeadCreate(BaseModel):
    business_name: str = Field(..., min_length=1, max_length=255)
    contact_name: Optional[str] = Field(default=None, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=64)
    email: Optional[str] = Field(default=None, max_length=255)
    website: Optional[str] = Field(default=None, max_length=500)
    address: Optional[str] = None
    country: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    niche: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=255)
    keyword: Optional[str] = Field(default=None, max_length=255)
    google_rating: Optional[float] = Field(default=None, ge=0, le=5)
    lead_source: Optional[str] = Field(default=None, max_length=100)
    timezone: Optional[str] = Field(default=None, max_length=64)
    extra_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("phone_number", "email", "website")
    @classmethod
    def empty_to_none(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            return None
        return value


class SalesLeadUpdate(BaseModel):
    contact_name: Optional[str] = Field(default=None, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=64)
    email: Optional[str] = Field(default=None, max_length=255)
    website: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=64)
    pipeline_stage: Optional[PipelineStage] = None
    quality_score: Optional[int] = Field(default=None, ge=0, le=100)
    qualification_score: Optional[int] = Field(default=None, ge=0, le=100)
    classification: Optional[Literal["hot", "warm", "cold"]] = None
    next_action: Optional[str] = Field(default=None, max_length=64)
    research_status: Optional[str] = Field(default=None, max_length=32)
    enrichment_status: Optional[str] = Field(default=None, max_length=32)
    extra_metadata: Optional[dict[str, Any]] = None


class SalesLeadResponse(BaseModel):
    id: int
    business_name: str
    contact_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    website: Optional[str]
    address: Optional[str]
    country: Optional[str]
    city: Optional[str]
    niche: Optional[str]
    category: Optional[str]
    google_rating: Optional[float]
    lead_source: Optional[str]
    status: str
    pipeline_stage: str
    quality_score: Optional[int]
    qualification_score: Optional[int]
    classification: Optional[str]
    next_action: Optional[str]
    research_status: str
    enrichment_status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SalesLeadsResponse(BaseModel):
    leads: list[SalesLeadResponse]
    total: int


class ResearchReportCreate(BaseModel):
    lead_id: int
    company_summary: Optional[str] = None
    pain_points: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    opening_lines: list[str] = Field(default_factory=list)
    pitch_suggestions: list[str] = Field(default_factory=list)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    raw_report: dict[str, Any] = Field(default_factory=dict)


class ResearchReportResponse(ResearchReportCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CampaignLeadAttachRequest(BaseModel):
    lead_ids: list[int] = Field(..., min_length=1, max_length=1000)


class CallCreate(BaseModel):
    lead_id: Optional[int] = None
    campaign_id: Optional[int] = None
    workflow_run_id: Optional[int] = None
    external_call_id: Optional[str] = Field(default=None, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=64)
    direction: Literal["outbound", "inbound"] = "outbound"
    status: str = Field(default="created", max_length=64)


class CallResponse(CallCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CallInsightCreate(BaseModel):
    call_id: int
    transcript_text: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = Field(default=None, max_length=32)
    buying_signals: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    qualification: dict[str, Any] = Field(default_factory=dict)
    qualification_score: Optional[int] = Field(default=None, ge=0, le=100)
    recommended_next_action: Optional[str] = Field(default=None, max_length=64)


class KnowledgeSourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    source_type: str = Field(..., max_length=64)
    category: str = Field(..., max_length=64)
    content: Optional[str] = None
    url: Optional[str] = Field(default=None, max_length=1000)
    knowledge_base_document_id: Optional[int] = None
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeSourceResponse(KnowledgeSourceCreate):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalyticsResponse(BaseModel):
    total_leads: int
    calls_made: int
    connected_calls: int
    interested_leads: int
    meetings_booked: int
    conversion_rate: float
    revenue_generated: float
    hot_leads: int
    warm_leads: int
    cold_leads: int
