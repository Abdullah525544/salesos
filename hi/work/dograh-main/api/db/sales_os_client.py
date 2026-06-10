from datetime import UTC, datetime
from typing import Any, Optional

from sqlalchemy import func, update
from sqlalchemy.future import select

from api.db.base_client import BaseDBClient
from api.db.models import (
    SalesActivityModel,
    SalesAgentRunModel,
    SalesCallInsightModel,
    SalesCallModel,
    SalesCallTranscriptModel,
    SalesCampaignLeadModel,
    SalesKnowledgeSourceModel,
    SalesLeadModel,
    SalesMeetingModel,
    SalesPipelineStageModel,
    SalesResearchReportModel,
)


DEFAULT_PIPELINE_STAGES = (
    ("new_lead", "New Lead", 10, False, False),
    ("contacted", "Contacted", 20, False, False),
    ("interested", "Interested", 30, False, False),
    ("meeting_scheduled", "Meeting Scheduled", 40, False, False),
    ("proposal_sent", "Proposal Sent", 50, False, False),
    ("closed_won", "Closed Won", 60, True, True),
    ("closed_lost", "Closed Lost", 70, True, False),
)


class SalesOSClient(BaseDBClient):
    async def ensure_sales_pipeline_stages(self, organization_id: int) -> None:
        async with self.async_session() as session:
            existing = await session.execute(
                select(SalesPipelineStageModel.key).where(
                    SalesPipelineStageModel.organization_id == organization_id
                )
            )
            existing_keys = set(existing.scalars().all())
            for key, name, position, is_closed, is_won in DEFAULT_PIPELINE_STAGES:
                if key in existing_keys:
                    continue
                session.add(
                    SalesPipelineStageModel(
                        organization_id=organization_id,
                        key=key,
                        name=name,
                        position=position,
                        is_closed=is_closed,
                        is_won=is_won,
                    )
                )
            await session.commit()

    async def create_sales_lead(
        self,
        *,
        organization_id: int,
        created_by: int,
        data: dict[str, Any],
    ) -> SalesLeadModel:
        async with self.async_session() as session:
            lead = SalesLeadModel(
                organization_id=organization_id,
                created_by=created_by,
                **data,
            )
            session.add(lead)
            await session.commit()
            await session.refresh(lead)
            return lead

    async def list_sales_leads(
        self,
        *,
        organization_id: int,
        limit: int = 50,
        offset: int = 0,
        pipeline_stage: Optional[str] = None,
        query: Optional[str] = None,
    ) -> tuple[list[SalesLeadModel], int]:
        async with self.async_session() as session:
            stmt = select(SalesLeadModel).where(
                SalesLeadModel.organization_id == organization_id,
                SalesLeadModel.archived_at.is_(None),
            )
            if pipeline_stage:
                stmt = stmt.where(SalesLeadModel.pipeline_stage == pipeline_stage)
            if query:
                pattern = f"%{query}%"
                stmt = stmt.where(
                    SalesLeadModel.business_name.ilike(pattern)
                    | SalesLeadModel.email.ilike(pattern)
                    | SalesLeadModel.phone_number.ilike(pattern)
                )

            total_stmt = stmt.with_only_columns(func.count(SalesLeadModel.id)).order_by(
                None
            )
            total = (await session.execute(total_stmt)).scalar() or 0
            result = await session.execute(
                stmt.order_by(SalesLeadModel.created_at.desc()).limit(limit).offset(offset)
            )
            return list(result.scalars().all()), total

    async def get_sales_lead(
        self, *, organization_id: int, lead_id: int
    ) -> Optional[SalesLeadModel]:
        async with self.async_session() as session:
            result = await session.execute(
                select(SalesLeadModel).where(
                    SalesLeadModel.id == lead_id,
                    SalesLeadModel.organization_id == organization_id,
                    SalesLeadModel.archived_at.is_(None),
                )
            )
            return result.scalar_one_or_none()

    async def update_sales_lead(
        self, *, organization_id: int, lead_id: int, data: dict[str, Any]
    ) -> Optional[SalesLeadModel]:
        async with self.async_session() as session:
            result = await session.execute(
                select(SalesLeadModel).where(
                    SalesLeadModel.id == lead_id,
                    SalesLeadModel.organization_id == organization_id,
                    SalesLeadModel.archived_at.is_(None),
                )
            )
            lead = result.scalar_one_or_none()
            if not lead:
                return None
            for key, value in data.items():
                if value is not None:
                    setattr(lead, key, value)
            await session.commit()
            await session.refresh(lead)
            return lead

    async def archive_sales_lead(self, *, organization_id: int, lead_id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(
                update(SalesLeadModel)
                .where(
                    SalesLeadModel.id == lead_id,
                    SalesLeadModel.organization_id == organization_id,
                    SalesLeadModel.archived_at.is_(None),
                )
                .values(archived_at=datetime.now(UTC))
            )
            await session.commit()
            return bool(result.rowcount)

    async def attach_leads_to_campaign(
        self, *, organization_id: int, campaign_id: int, lead_ids: list[int]
    ) -> int:
        async with self.async_session() as session:
            count = 0
            for lead_id in lead_ids:
                exists = await session.execute(
                    select(SalesCampaignLeadModel.id).where(
                        SalesCampaignLeadModel.campaign_id == campaign_id,
                        SalesCampaignLeadModel.lead_id == lead_id,
                    )
                )
                if exists.scalar_one_or_none():
                    continue
                session.add(
                    SalesCampaignLeadModel(
                        organization_id=organization_id,
                        campaign_id=campaign_id,
                        lead_id=lead_id,
                    )
                )
                count += 1
            await session.commit()
            return count

    async def create_research_report(
        self, *, organization_id: int, data: dict[str, Any]
    ) -> SalesResearchReportModel:
        async with self.async_session() as session:
            report = SalesResearchReportModel(organization_id=organization_id, **data)
            session.add(report)
            await session.execute(
                update(SalesLeadModel)
                .where(
                    SalesLeadModel.id == data["lead_id"],
                    SalesLeadModel.organization_id == organization_id,
                )
                .values(research_status="completed")
            )
            await session.commit()
            await session.refresh(report)
            return report

    async def create_sales_call(
        self, *, organization_id: int, data: dict[str, Any]
    ) -> SalesCallModel:
        async with self.async_session() as session:
            call = SalesCallModel(organization_id=organization_id, **data)
            session.add(call)
            await session.commit()
            await session.refresh(call)
            return call

    async def save_call_intelligence(
        self, *, organization_id: int, data: dict[str, Any]
    ) -> SalesCallInsightModel:
        async with self.async_session() as session:
            call = await session.get(SalesCallModel, data["call_id"])
            if not call or call.organization_id != organization_id:
                raise ValueError("Call not found")

            transcript_text = data.pop("transcript_text", None)
            if transcript_text:
                session.add(
                    SalesCallTranscriptModel(
                        organization_id=organization_id,
                        call_id=call.id,
                        transcript_text=transcript_text,
                    )
                )

            insight = SalesCallInsightModel(
                organization_id=organization_id,
                lead_id=call.lead_id,
                **data,
            )
            session.add(insight)
            if call.lead_id and data.get("qualification_score") is not None:
                score = int(data["qualification_score"])
                classification = "hot" if score >= 75 else "warm" if score >= 40 else "cold"
                next_action = data.get("recommended_next_action")
                await session.execute(
                    update(SalesLeadModel)
                    .where(
                        SalesLeadModel.id == call.lead_id,
                        SalesLeadModel.organization_id == organization_id,
                    )
                    .values(
                        qualification_score=score,
                        classification=classification,
                        next_action=next_action,
                    )
                )
            await session.commit()
            await session.refresh(insight)
            return insight

    async def create_knowledge_source(
        self,
        *,
        organization_id: int,
        created_by: int,
        data: dict[str, Any],
    ) -> SalesKnowledgeSourceModel:
        async with self.async_session() as session:
            source = SalesKnowledgeSourceModel(
                organization_id=organization_id, created_by=created_by, **data
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)
            return source

    async def list_knowledge_sources(
        self, *, organization_id: int
    ) -> list[SalesKnowledgeSourceModel]:
        async with self.async_session() as session:
            result = await session.execute(
                select(SalesKnowledgeSourceModel)
                .where(
                    SalesKnowledgeSourceModel.organization_id == organization_id,
                    SalesKnowledgeSourceModel.is_active.is_(True),
                )
                .order_by(SalesKnowledgeSourceModel.created_at.desc())
            )
            return list(result.scalars().all())

    async def create_agent_run(
        self, *, organization_id: int, agent_type: str, input_data: dict[str, Any]
    ) -> SalesAgentRunModel:
        async with self.async_session() as session:
            run = SalesAgentRunModel(
                organization_id=organization_id,
                agent_type=agent_type,
                status="queued",
                input=input_data,
            )
            session.add(run)
            await session.commit()
            await session.refresh(run)
            return run

    async def create_activity(
        self,
        *,
        organization_id: int,
        lead_id: int,
        activity_type: str,
        title: str,
        body: Optional[str] = None,
        actor_type: str = "agent",
        extra_metadata: Optional[dict[str, Any]] = None,
    ) -> SalesActivityModel:
        async with self.async_session() as session:
            activity = SalesActivityModel(
                organization_id=organization_id,
                lead_id=lead_id,
                actor_type=actor_type,
                activity_type=activity_type,
                title=title,
                body=body,
                extra_metadata=extra_metadata or {},
            )
            session.add(activity)
            await session.commit()
            await session.refresh(activity)
            return activity

    async def get_sales_analytics(self, *, organization_id: int) -> dict[str, Any]:
        async with self.async_session() as session:
            total_leads = (
                await session.execute(
                    select(func.count(SalesLeadModel.id)).where(
                        SalesLeadModel.organization_id == organization_id,
                        SalesLeadModel.archived_at.is_(None),
                    )
                )
            ).scalar() or 0
            calls_made = (
                await session.execute(
                    select(func.count(SalesCallModel.id)).where(
                        SalesCallModel.organization_id == organization_id
                    )
                )
            ).scalar() or 0
            connected_calls = (
                await session.execute(
                    select(func.count(SalesCallModel.id)).where(
                        SalesCallModel.organization_id == organization_id,
                        SalesCallModel.status.in_(["connected", "completed"]),
                    )
                )
            ).scalar() or 0
            interested_leads = (
                await session.execute(
                    select(func.count(SalesLeadModel.id)).where(
                        SalesLeadModel.organization_id == organization_id,
                        SalesLeadModel.pipeline_stage.in_(
                            ["interested", "meeting_scheduled", "proposal_sent", "closed_won"]
                        ),
                    )
                )
            ).scalar() or 0
            meetings_booked = (
                await session.execute(
                    select(func.count(SalesMeetingModel.id)).where(
                        SalesMeetingModel.organization_id == organization_id
                    )
                )
            ).scalar() or 0
            hot_leads = await self._count_classification(session, organization_id, "hot")
            warm_leads = await self._count_classification(session, organization_id, "warm")
            cold_leads = await self._count_classification(session, organization_id, "cold")
            conversion_rate = (meetings_booked / total_leads * 100) if total_leads else 0.0
            return {
                "total_leads": total_leads,
                "calls_made": calls_made,
                "connected_calls": connected_calls,
                "interested_leads": interested_leads,
                "meetings_booked": meetings_booked,
                "conversion_rate": round(conversion_rate, 2),
                "revenue_generated": 0.0,
                "hot_leads": hot_leads,
                "warm_leads": warm_leads,
                "cold_leads": cold_leads,
            }

    async def _count_classification(self, session, organization_id: int, value: str) -> int:
        return (
            await session.execute(
                select(func.count(SalesLeadModel.id)).where(
                    SalesLeadModel.organization_id == organization_id,
                    SalesLeadModel.classification == value,
                )
            )
        ).scalar() or 0
