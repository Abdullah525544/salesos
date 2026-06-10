from fastapi import APIRouter, Depends, HTTPException, Query

from api.db import db_client
from api.db.models import UserModel
from api.schemas.sales_os import (
    AnalyticsResponse,
    CallCreate,
    CallInsightCreate,
    CallResponse,
    CampaignLeadAttachRequest,
    KnowledgeSourceCreate,
    KnowledgeSourceResponse,
    LeadFinderRequest,
    ResearchReportCreate,
    ResearchReportResponse,
    SalesLeadCreate,
    SalesLeadResponse,
    SalesLeadsResponse,
    SalesLeadUpdate,
)
from api.sdk_expose import sdk_expose
from api.services.auth.depends import get_user

router = APIRouter(prefix="/sales-os", tags=["sales-os"])


def _org_id(user: UserModel) -> int:
    if not user.selected_organization_id:
        raise HTTPException(status_code=400, detail="No organization selected")
    return user.selected_organization_id


@router.post(
    "/lead-finder/search",
    response_model=SalesLeadsResponse,
    **sdk_expose(
        method="search_sales_leads",
        description="Create a lead-finder agent run for a niche/location query.",
    ),
)
async def search_leads(
    request: LeadFinderRequest,
    user: UserModel = Depends(get_user),
) -> SalesLeadsResponse:
    organization_id = _org_id(user)
    await db_client.create_agent_run(
        organization_id=organization_id,
        agent_type="lead_finder",
        input_data=request.model_dump(),
    )
    leads, total = await db_client.list_sales_leads(
        organization_id=organization_id,
        limit=request.limit,
        query=request.niche,
    )
    return SalesLeadsResponse(leads=leads, total=total)


@router.post("/leads", response_model=SalesLeadResponse)
async def create_lead(
    request: SalesLeadCreate,
    user: UserModel = Depends(get_user),
) -> SalesLeadResponse:
    organization_id = _org_id(user)
    await db_client.ensure_sales_pipeline_stages(organization_id)
    lead = await db_client.create_sales_lead(
        organization_id=organization_id,
        created_by=user.id,
        data=request.model_dump(),
    )
    await db_client.create_activity(
        organization_id=organization_id,
        lead_id=lead.id,
        activity_type="lead_created",
        title="Lead created",
        body=f"{lead.business_name} entered the CRM.",
    )
    return lead


@router.get("/leads", response_model=SalesLeadsResponse)
async def list_leads(
    limit: int = Query(default=50, ge=1, le=250),
    offset: int = Query(default=0, ge=0),
    pipeline_stage: str | None = None,
    query: str | None = None,
    user: UserModel = Depends(get_user),
) -> SalesLeadsResponse:
    leads, total = await db_client.list_sales_leads(
        organization_id=_org_id(user),
        limit=limit,
        offset=offset,
        pipeline_stage=pipeline_stage,
        query=query,
    )
    return SalesLeadsResponse(leads=leads, total=total)


@router.get("/leads/{lead_id}", response_model=SalesLeadResponse)
async def get_lead(
    lead_id: int,
    user: UserModel = Depends(get_user),
) -> SalesLeadResponse:
    lead = await db_client.get_sales_lead(organization_id=_org_id(user), lead_id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/leads/{lead_id}", response_model=SalesLeadResponse)
async def update_lead(
    lead_id: int,
    request: SalesLeadUpdate,
    user: UserModel = Depends(get_user),
) -> SalesLeadResponse:
    lead = await db_client.update_sales_lead(
        organization_id=_org_id(user),
        lead_id=lead_id,
        data=request.model_dump(exclude_unset=True),
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.delete("/leads/{lead_id}")
async def archive_lead(
    lead_id: int,
    user: UserModel = Depends(get_user),
) -> dict[str, bool]:
    archived = await db_client.archive_sales_lead(
        organization_id=_org_id(user), lead_id=lead_id
    )
    if not archived:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"archived": True}


@router.post("/campaigns/{campaign_id}/leads")
async def attach_campaign_leads(
    campaign_id: int,
    request: CampaignLeadAttachRequest,
    user: UserModel = Depends(get_user),
) -> dict[str, int]:
    campaign = await db_client.get_campaign(campaign_id, _org_id(user))
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    attached = await db_client.attach_leads_to_campaign(
        organization_id=_org_id(user),
        campaign_id=campaign_id,
        lead_ids=request.lead_ids,
    )
    return {"attached": attached}


@router.post("/research/reports", response_model=ResearchReportResponse)
async def create_research_report(
    request: ResearchReportCreate,
    user: UserModel = Depends(get_user),
) -> ResearchReportResponse:
    lead = await db_client.get_sales_lead(
        organization_id=_org_id(user), lead_id=request.lead_id
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    report = await db_client.create_research_report(
        organization_id=_org_id(user), data=request.model_dump()
    )
    await db_client.create_activity(
        organization_id=_org_id(user),
        lead_id=request.lead_id,
        activity_type="research_completed",
        title="Prospect research completed",
        body=report.company_summary,
    )
    return report


@router.post("/calls", response_model=CallResponse)
async def create_call(
    request: CallCreate,
    user: UserModel = Depends(get_user),
) -> CallResponse:
    return await db_client.create_sales_call(
        organization_id=_org_id(user), data=request.model_dump()
    )


@router.post("/calls/intelligence")
async def save_call_intelligence(
    request: CallInsightCreate,
    user: UserModel = Depends(get_user),
) -> dict[str, int]:
    try:
        insight = await db_client.save_call_intelligence(
            organization_id=_org_id(user),
            data=request.model_dump(exclude_none=True),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"insight_id": insight.id}


@router.post("/knowledge-sources", response_model=KnowledgeSourceResponse)
async def create_knowledge_source(
    request: KnowledgeSourceCreate,
    user: UserModel = Depends(get_user),
) -> KnowledgeSourceResponse:
    return await db_client.create_knowledge_source(
        organization_id=_org_id(user),
        created_by=user.id,
        data=request.model_dump(),
    )


@router.get("/knowledge-sources", response_model=list[KnowledgeSourceResponse])
async def list_knowledge_sources(
    user: UserModel = Depends(get_user),
) -> list[KnowledgeSourceResponse]:
    return await db_client.list_knowledge_sources(organization_id=_org_id(user))


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_sales_analytics(
    user: UserModel = Depends(get_user),
) -> AnalyticsResponse:
    return await db_client.get_sales_analytics(organization_id=_org_id(user))
