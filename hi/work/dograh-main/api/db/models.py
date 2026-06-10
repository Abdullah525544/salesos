import uuid
from datetime import UTC, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    and_,
    func,
    text,
)
from sqlalchemy.orm import declarative_base, relationship

from api.constants import DEFAULT_CAMPAIGN_RETRY_CONFIG

from ..enums import (
    CallType,
    IntegrationAction,
    ToolCategory,
    ToolStatus,
    TriggerState,
    WebhookCredentialType,
    WorkflowRunState,
    WorkflowStatus,
)

Base = declarative_base()


# TODO: remove workflow_defintion after migration, remove nullable workflow_defintion_id from Workflow and Workflowrun


# Association table for many-to-many relationship between users and organizations
organization_users_association = Table(
    "organization_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column(
        "organization_id", Integer, ForeignKey("organizations.id"), primary_key=True
    ),
)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    workflows = relationship("WorkflowModel", back_populates="user")
    selected_organization_id = Column(
        Integer, ForeignKey("organizations.id"), nullable=True
    )
    selected_organization = relationship("OrganizationModel", back_populates="users")
    organizations = relationship(
        "OrganizationModel",
        secondary=organization_users_association,
        back_populates="users",
    )
    is_superuser = Column(Boolean, default=False)
    email = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)

    __table_args__ = (
        Index(
            "ix_users_email_lower",
            func.lower(email),
            unique=True,
            postgresql_where=text("email IS NOT NULL"),
        ),
    )


class UserConfigurationModel(Base):
    __tablename__ = "user_configurations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    configuration = Column(JSON, nullable=False, default=dict)
    last_validated_at = Column(DateTime(timezone=True), nullable=True)


# New Organization model
class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Quota fields
    quota_type = Column(
        Enum("monthly", "annual", name="quota_type"),
        nullable=False,
        default="monthly",
        server_default=text("'monthly'::quota_type"),
    )
    quota_dograh_tokens = Column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    quota_reset_day = Column(
        Integer, nullable=False, default=1, server_default=text("1")
    )  # 1-28, only for monthly
    quota_start_date = Column(DateTime(timezone=True), nullable=True)  # Only for annual
    quota_enabled = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    price_per_second_usd = Column(Float, nullable=True)

    # Relationships
    users = relationship(
        "UserModel",
        secondary=organization_users_association,
        back_populates="organizations",
    )
    integrations = relationship("IntegrationModel", back_populates="organization")
    usage_cycles = relationship(
        "OrganizationUsageCycleModel", back_populates="organization"
    )
    configurations = relationship(
        "OrganizationConfigurationModel", back_populates="organization"
    )
    api_keys = relationship("APIKeyModel", back_populates="organization")


class APIKeyModel(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    key_hash = Column(String, nullable=False, unique=True, index=True)
    key_prefix = Column(String, nullable=False)  # Store first 8 chars for display
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    archived_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    organization = relationship("OrganizationModel", back_populates="api_keys")
    created_by_user = relationship("UserModel")

    # Indexes for performance
    __table_args__ = (
        Index("ix_api_keys_organization_id", "organization_id"),
        Index("ix_api_keys_key_hash", "key_hash"),
        Index("ix_api_keys_active", "is_active"),
    )


class OrganizationConfigurationModel(Base):
    __tablename__ = "organization_configurations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    key = Column(String, nullable=False)
    value = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    organization = relationship("OrganizationModel", back_populates="configurations")

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint("organization_id", "key", name="_organization_key_uc"),
        Index("ix_organization_configurations_organization_id", "organization_id"),
    )


class TelephonyConfigurationModel(Base):
    __tablename__ = "telephony_configurations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(64), nullable=False)
    provider = Column(String(32), nullable=False)
    credentials = Column(JSON, nullable=False, default=dict)
    is_default_outbound = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    organization = relationship("OrganizationModel")
    phone_numbers = relationship(
        "TelephonyPhoneNumberModel",
        back_populates="configuration",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "organization_id", "name", name="uq_telephony_configurations_org_name"
        ),
        Index("ix_telephony_configurations_org", "organization_id"),
        Index(
            "uq_telephony_configurations_default",
            "organization_id",
            unique=True,
            postgresql_where=text("is_default_outbound = true"),
        ),
    )


class TelephonyPhoneNumberModel(Base):
    __tablename__ = "telephony_phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    telephony_configuration_id = Column(
        Integer,
        ForeignKey("telephony_configurations.id", ondelete="CASCADE"),
        nullable=False,
    )
    address = Column(String(255), nullable=False)
    address_normalized = Column(String(255), nullable=False)
    address_type = Column(String(16), nullable=False)
    country_code = Column(String(2), nullable=True)
    label = Column(String(64), nullable=True)
    inbound_workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_active = Column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    is_default_caller_id = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    configuration = relationship(
        "TelephonyConfigurationModel", back_populates="phone_numbers"
    )
    inbound_workflow = relationship("WorkflowModel")

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "address_normalized",
            name="uq_phone_numbers_org_address",
        ),
        Index("ix_phone_numbers_config", "telephony_configuration_id"),
        Index(
            "ix_phone_numbers_workflow",
            "inbound_workflow_id",
            postgresql_where=text("inbound_workflow_id IS NOT NULL"),
        ),
        Index(
            "ix_phone_numbers_inbound_lookup",
            "address_normalized",
            "organization_id",
            postgresql_where=text("is_active = true"),
        ),
        Index(
            "uq_phone_numbers_default_caller",
            "telephony_configuration_id",
            unique=True,
            postgresql_where=text("is_default_caller_id = true"),
        ),
    )


class IntegrationModel(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    integration_id = Column(
        String, nullable=False, index=True
    )  # External connection ID
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    provider = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    connection_details = Column(JSON, nullable=False, default=dict)
    action = Column(String, nullable=False, default=IntegrationAction.ALL_CALLS.value)

    # Relationships
    organization = relationship("OrganizationModel", back_populates="integrations")


class WorkflowDefinitionModel(Base):
    __tablename__ = "workflow_definitions"
    id = Column(Integer, primary_key=True, index=True)
    workflow_hash = Column(String, nullable=True)  # Legacy, no longer used
    workflow_json = Column(JSON, nullable=False, default=dict)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)
    is_current = Column(
        Boolean, default=False, nullable=False, server_default=text("false")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Versioning columns
    status = Column(
        String,
        nullable=False,
        default="published",
        server_default=text("'published'"),
    )  # draft | published | archived
    version_number = Column(
        Integer, nullable=True
    )  # Sequential per workflow, display only
    published_at = Column(DateTime(timezone=True), nullable=True)

    # Full behavioral snapshot (moved from WorkflowModel to enable versioning)
    workflow_configurations = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    template_context_variables = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )

    # Table constraints and indexes — unique hash constraint removed (no more dedup)
    __table_args__ = (
        Index("ix_workflow_definitions_workflow_status", "workflow_id", "status"),
    )

    # Relationships
    workflow = relationship(
        "WorkflowModel",
        back_populates="definitions",
        foreign_keys=[workflow_id],
    )
    workflow_runs = relationship("WorkflowRunModel", back_populates="definition")


class FolderModel(Base):
    """A folder for grouping workflows (agents) within an organization.

    Folders are flat (no nesting) and org-scoped. A workflow belongs to at
    most one folder via ``WorkflowModel.folder_id``; a NULL folder_id means
    the workflow is "Uncategorized".
    """

    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )
    organization = relationship("OrganizationModel")
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    workflows = relationship("WorkflowModel", back_populates="folder")

    # Folder names must be unique within an organization.
    __table_args__ = (
        UniqueConstraint("organization_id", "name", name="uq_folder_org_name"),
    )


class WorkflowModel(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("UserModel", back_populates="workflows")
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("OrganizationModel")
    # Optional folder for grouping in the agents list. NULL = "Uncategorized".
    # ON DELETE SET NULL: deleting a folder un-files its agents, never deletes them.
    folder_id = Column(
        Integer,
        ForeignKey("folders.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    folder = relationship("FolderModel", back_populates="workflows")
    name = Column(String, index=True, nullable=False)
    status = Column(
        Enum(*[status.value for status in WorkflowStatus], name="workflow_status"),
        nullable=False,
        default=WorkflowStatus.ACTIVE.value,
        server_default=text("'active'::workflow_status"),
    )
    workflow_definition = Column(JSON, nullable=False, default=dict)
    template_context_variables = Column(JSON, nullable=False, default=dict)
    call_disposition_codes = Column(JSON, nullable=False, default=dict)
    workflow_configurations = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    runs = relationship("WorkflowRunModel", back_populates="workflow")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Pointer to the currently-live (published) version
    released_definition_id = Column(
        Integer,
        ForeignKey("workflow_definitions.id", use_alter=True),
        nullable=True,
    )
    released_definition = relationship(
        "WorkflowDefinitionModel",
        foreign_keys=[released_definition_id],
        uselist=False,
        viewonly=True,
    )

    # All versions / historical definitions of this workflow
    definitions = relationship(
        "WorkflowDefinitionModel",
        back_populates="workflow",
        foreign_keys="WorkflowDefinitionModel.workflow_id",
    )

    # Relationship to fetch the current (is_current=True) definition
    # Kept for backward compatibility during transition
    current_definition = relationship(
        "WorkflowDefinitionModel",
        primaryjoin=lambda: and_(
            WorkflowDefinitionModel.workflow_id == WorkflowModel.id,
            WorkflowDefinitionModel.is_current.is_(True),
        ),
        uselist=False,
        viewonly=True,
    )

    @property
    def current_definition_id(self):
        """Return ID of the current workflow definition (helper for backwards-compat)."""
        current_def = self.__dict__.get("current_definition")
        if current_def is not None:
            return current_def.id

        # If relationship is not loaded, we cannot safely access definitions without
        # risking an implicit lazy load on a detached instance. Return ``None`` in
        # that scenario so callers can handle the absence explicitly.
        return None


class WorkflowTemplates(Base):
    __tablename__ = "workflow_templates"
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, nullable=False, index=True)
    template_description = Column(String, nullable=False, index=True)
    template_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class WorkflowRunModel(Base):
    __tablename__ = "workflow_runs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    workflow = relationship("WorkflowModel", back_populates="runs")
    definition_id = Column(
        Integer, ForeignKey("workflow_definitions.id"), nullable=True
    )
    definition = relationship("WorkflowDefinitionModel", back_populates="workflow_runs")
    # Stored as VARCHAR (not a Postgres ENUM) so new telephony providers can
    # be added purely in application code without a database migration.
    # See WorkflowRunMode in api/enums.py for the canonical value set.
    mode = Column(String(64), nullable=False)
    call_type = Column(
        Enum(*[call_type.value for call_type in CallType], name="workflow_call_type"),
        nullable=False,
        default=CallType.OUTBOUND.value,
        server_default=text("'outbound'::workflow_call_type"),
    )
    state = Column(
        Enum(*[state.value for state in WorkflowRunState], name="workflow_run_state"),
        nullable=False,
        default=WorkflowRunState.INITIALIZED.value,
        server_default=text("'initialized'::workflow_run_state"),
    )
    is_completed = Column(Boolean, default=False)
    recording_url = Column(String, nullable=True)
    transcript_url = Column(String, nullable=True)
    # Store storage backend as string enum (s3, minio)
    storage_backend = Column(
        Enum("s3", "minio", name="storage_backend"),
        nullable=False,
        default="s3",
        server_default=text("'s3'::storage_backend"),
    )
    usage_info = Column(JSON, nullable=False, default=dict)
    cost_info = Column(JSON, nullable=False, default=dict)
    initial_context = Column(JSON, nullable=False, default=dict)
    gathered_context = Column(JSON, nullable=False, default=dict)
    logs = Column(JSON, nullable=False, default=dict, server_default=text("'{}'::json"))
    annotations = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    campaign = relationship("CampaignModel")
    queued_run_id = Column(Integer, ForeignKey("queued_runs.id"), nullable=True)
    queued_run = relationship("QueuedRunModel", foreign_keys=[queued_run_id])
    public_access_token = Column(String(36), nullable=True)
    text_session = relationship(
        "WorkflowRunTextSessionModel",
        back_populates="workflow_run",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        Index(
            "idx_workflow_runs_public_access_token",
            "public_access_token",
            unique=True,
            postgresql_where=text("public_access_token IS NOT NULL"),
        ),
        Index(
            "idx_workflow_runs_call_id",
            text("(gathered_context->>'call_id')"),
            postgresql_where=text("gathered_context->>'call_id' IS NOT NULL"),
        ),
        Index("idx_workflow_runs_workflow_id", "workflow_id"),
        Index("idx_workflow_runs_campaign_id", "campaign_id"),
    )


class WorkflowRunTextSessionModel(Base):
    __tablename__ = "workflow_run_text_sessions"

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    workflow_run = relationship("WorkflowRunModel", back_populates="text_session")
    revision = Column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    session_data = Column(
        JSON,
        nullable=False,
        default=dict,
        server_default=text("'{}'::json"),
    )
    checkpoint = Column(
        JSON,
        nullable=False,
        default=dict,
        server_default=text("'{}'::json"),
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    __table_args__ = (Index("ix_workflow_run_text_sessions_updated_at", "updated_at"),)


class OrganizationUsageCycleModel(Base):
    """
    This model is used to track the usage of Dograh tokens for an organization for a given usage
    cycle.
    """

    __tablename__ = "organization_usage_cycles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    quota_dograh_tokens = Column(Integer, nullable=False)
    used_dograh_tokens = Column(Float, nullable=False, default=0)
    total_duration_seconds = Column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    # New USD tracking fields
    used_amount_usd = Column(Float, nullable=True, default=0)
    quota_amount_usd = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    organization = relationship("OrganizationModel", back_populates="usage_cycles")

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint(
            "organization_id", "period_start", "period_end", name="unique_org_period"
        ),
        Index("idx_usage_cycles_org_period", "organization_id", "period_end"),
    )


class CampaignModel(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Nullable during the legacy → multi-config migration window. Backfilled to the
    # org's default config by the migration; will become NOT NULL in a follow-up.
    telephony_configuration_id = Column(
        Integer, ForeignKey("telephony_configurations.id"), nullable=True
    )

    # Source configuration
    source_type = Column(String, nullable=False, default="csv")
    source_id = Column(String, nullable=False)  # CSV file key

    # State management
    state = Column(
        Enum(
            "created",
            "syncing",
            "running",
            "paused",
            "completed",
            "failed",
            name="campaign_state",
        ),
        nullable=False,
        default="created",
    )

    # Progress tracking
    total_rows = Column(Integer, nullable=True)
    processed_rows = Column(Integer, nullable=False, default=0)
    failed_rows = Column(Integer, nullable=False, default=0)

    # Rate limiting and sync configuration
    rate_limit_per_second = Column(Integer, nullable=False, default=1)
    max_retries = Column(Integer, nullable=False, default=0)
    source_sync_status = Column(String, nullable=False, default="pending")
    source_last_synced_at = Column(DateTime(timezone=True), nullable=True)
    source_sync_error = Column(String, nullable=True)

    # Retry configuration for call failures
    retry_config = Column(
        JSON,
        nullable=False,
        default=DEFAULT_CAMPAIGN_RETRY_CONFIG,
        server_default=text(
            '\'{"enabled": true, "max_retries": 2, "retry_on_busy": true, "retry_on_no_answer": true, "retry_on_voicemail": true, "retry_delay_seconds": 120}\'::jsonb'
        ),
    )

    # Orchestrator tracking fields
    last_batch_scheduled_at = Column(DateTime(timezone=True), nullable=True)
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    orchestrator_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )

    # Append-only timestamped log entries for state transitions, failures,
    # and circuit-breaker events. Surfaced in the UI so operators can see
    # why a campaign moved to paused/failed without digging through logs.
    logs = Column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'::json"),
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    organization = relationship("OrganizationModel")
    workflow = relationship("WorkflowModel")
    created_by_user = relationship("UserModel")

    # Indexes
    __table_args__ = (
        Index("ix_campaigns_org_id", "organization_id"),
        Index("ix_campaigns_state", "state"),
        Index("ix_campaigns_workflow_id", "workflow_id"),
        Index(
            "ix_campaigns_telephony_config",
            "telephony_configuration_id",
            postgresql_where=text("telephony_configuration_id IS NOT NULL"),
        ),
        # Index for efficient querying of active campaigns
        Index(
            "idx_campaigns_active_status",
            "state",
            postgresql_where=text("state IN ('syncing', 'running', 'paused')"),
        ),
    )


class QueuedRunModel(Base):
    __tablename__ = "queued_runs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    source_uuid = Column(String, nullable=False)
    context_variables = Column(JSON, nullable=False, default=dict)
    state = Column(
        Enum("queued", "processed", "processing", "failed", name="queued_run_state"),
        nullable=False,
        default="queued",
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # New retry-related fields
    retry_count = Column(Integer, default=0, nullable=False, server_default=text("0"))
    parent_queued_run_id = Column(Integer, ForeignKey("queued_runs.id"), nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    retry_reason = Column(String, nullable=True)  # 'busy', 'no_answer', 'voicemail'

    # Relationships
    campaign = relationship("CampaignModel")
    parent_queued_run = relationship("QueuedRunModel", remote_side=[id])

    # Indexes
    __table_args__ = (
        Index("idx_queued_runs_campaign_state", "campaign_id", "state"),
        Index("idx_queued_runs_created", "created_at"),
        Index("idx_queued_runs_source_uuid", "source_uuid"),
        Index(
            "idx_queued_runs_scheduled", "scheduled_for"
        ),  # New index for scheduled retries
        # Optimized index for checking queued runs efficiently
        Index(
            "idx_queued_runs_campaign_state_optimized",
            "campaign_id",
            "state",
            postgresql_where=text("state = 'queued'"),
        ),
        # Optimized index for scheduled retries
        Index(
            "idx_queued_runs_scheduled_optimized",
            "campaign_id",
            "scheduled_for",
            postgresql_where=text("scheduled_for IS NOT NULL"),
        ),
        UniqueConstraint(
            "campaign_id",
            "source_uuid",
            "retry_count",
            name="unique_campaign_source_retry",
        ),
    )


class EmbedTokenModel(Base):
    """Model for storing workflow embed tokens"""

    __tablename__ = "embed_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    allowed_domains = Column(JSON, nullable=True)  # Array of whitelisted domains
    settings = Column(JSON, nullable=True)  # Widget customization settings
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    usage_limit = Column(Integer, nullable=True)  # Optional usage limit
    usage_count = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    created_by = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    workflow = relationship("WorkflowModel")
    organization = relationship("OrganizationModel")
    creator = relationship("UserModel")
    sessions = relationship(
        "EmbedSessionModel", back_populates="embed_token", cascade="all, delete-orphan"
    )


class EmbedSessionModel(Base):
    """Model for storing temporary embed sessions"""

    __tablename__ = "embed_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    embed_token_id = Column(
        Integer, ForeignKey("embed_tokens.id", ondelete="CASCADE"), nullable=False
    )
    workflow_run_id = Column(
        Integer, ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=True
    )
    client_ip = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    origin = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Relationships
    embed_token = relationship("EmbedTokenModel", back_populates="sessions")
    workflow_run = relationship("WorkflowRunModel")


class AgentTriggerModel(Base):
    """Model for storing agent trigger mappings (UUID -> workflow_id).

    This is a minimal lookup table that maps trigger UUIDs to workflows.
    The trigger node in the workflow definition is the source of truth.
    """

    __tablename__ = "agent_triggers"

    id = Column(Integer, primary_key=True, index=True)

    # Globally unique trigger path (UUID format)
    trigger_path = Column(String(36), unique=True, nullable=False, index=True)

    # Link to workflow
    workflow_id = Column(
        Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False
    )
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # State management (active/archived)
    state = Column(
        Enum(*[state.value for state in TriggerState], name="trigger_state"),
        nullable=False,
        default=TriggerState.ACTIVE.value,
        server_default=text("'active'::trigger_state"),
    )

    # Audit
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Relationships
    workflow = relationship("WorkflowModel")
    organization = relationship("OrganizationModel")

    # Indexes for performance
    __table_args__ = (
        Index("ix_agent_triggers_workflow_id", "workflow_id"),
        Index("ix_agent_triggers_state", "state"),
    )


class ExternalCredentialModel(Base):
    """Model for storing external authentication credentials.

    Credentials are stored separately from webhook configurations to allow
    reuse across multiple workflows and secure storage of sensitive data.
    """

    __tablename__ = "external_credentials"

    id = Column(Integer, primary_key=True, index=True)

    # Public UUID reference (used in APIs and workflow definitions)
    # This prevents enumeration attacks and hides internal IDs
    credential_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    # Organization scoping
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Credential metadata
    name = Column(String, nullable=False)  # Display name, e.g., "Salesforce API"
    description = Column(String, nullable=True)  # Optional description

    # Credential type - uses enum from api/enums.py
    credential_type = Column(
        Enum(
            *[t.value for t in WebhookCredentialType],
            name="webhook_credential_type",
        ),
        nullable=False,
        default=WebhookCredentialType.NONE.value,
    )

    # Encrypted credential data (JSON)
    # Structure depends on credential_type:
    # - api_key: {"header_name": "X-API-Key", "api_key": "value"}
    # - bearer_token: {"token": "value"}
    # - basic_auth: {"username": "user", "password": "value"}
    # - custom_header: {"header_name": "X-Custom", "header_value": "value"}
    credential_data = Column(JSON, nullable=False, default=dict)

    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Soft delete for safety
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    organization = relationship("OrganizationModel")
    created_by_user = relationship("UserModel")

    # Indexes and constraints
    __table_args__ = (
        Index("ix_webhook_credentials_organization_id", "organization_id"),
        Index("ix_webhook_credentials_uuid", "credential_uuid"),
        UniqueConstraint("organization_id", "name", name="unique_org_credential_name"),
    )


class ToolModel(Base):
    """Model for storing reusable tools that can be invoked during workflows.

    Tools provide a standardized way to integrate external functionality - from
    HTTP API calls to native integrations.
    """

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)

    # Public identifier (used in APIs and workflow references)
    tool_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    # Organization scoping
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Tool metadata
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    # Tool category - uses enum from api/enums.py
    category = Column(
        Enum(
            *[c.value for c in ToolCategory],
            name="tool_category",
        ),
        nullable=False,
        default=ToolCategory.HTTP_API.value,
    )

    # Icon configuration (for UI display)
    icon = Column(String(50), nullable=True)  # Icon identifier
    icon_color = Column(String(7), nullable=True)  # Hex color code

    # Status management
    status = Column(
        Enum(
            *[s.value for s in ToolStatus],
            name="tool_status",
        ),
        nullable=False,
        default=ToolStatus.ACTIVE.value,
        server_default=text("'active'::tool_status"),
    )

    # The tool definition (JSONB) - contains schema_version for compatibility
    # Structure depends on category:
    # - http_api: {"schema_version": 1, "type": "http_api", "config": {...}}
    definition = Column(JSON, nullable=False, default=dict)

    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    organization = relationship("OrganizationModel")
    created_by_user = relationship("UserModel")

    # Indexes and constraints
    __table_args__ = (
        Index("ix_tools_organization_id", "organization_id"),
        Index("ix_tools_uuid", "tool_uuid"),
        Index("ix_tools_status", "status"),
        Index("ix_tools_category", "category"),
    )


class KnowledgeBaseDocumentModel(Base):
    """Model for storing document-level metadata in the knowledge base.

    Each document represents a source file (PDF, DOCX, etc.) that has been
    processed and chunked for retrieval.
    """

    __tablename__ = "knowledge_base_documents"

    id = Column(Integer, primary_key=True, index=True)

    # Public identifier for API references
    document_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    # Organization scoping
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Document metadata
    filename = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    file_hash = Column(String(64), nullable=True)  # SHA-256 hash for deduplication
    mime_type = Column(String(100), nullable=True)

    # Retrieval mode: "chunked" (vector search) or "full_document" (return full text)
    retrieval_mode = Column(
        String(20), nullable=False, default="chunked", server_default="chunked"
    )
    full_text = Column(
        Text, nullable=True
    )  # Stored when retrieval_mode is "full_document"

    # Processing metadata
    source_url = Column(String, nullable=True)  # If document was fetched from URL
    total_chunks = Column(Integer, nullable=False, default=0)
    processing_status = Column(
        Enum(
            "pending",
            "processing",
            "completed",
            "failed",
            name="document_processing_status",
        ),
        nullable=False,
        default="pending",
        server_default=text("'pending'::document_processing_status"),
    )
    processing_error = Column(Text, nullable=True)

    # Docling conversion metadata
    docling_metadata = Column(
        JSON, nullable=False, default=dict
    )  # Store docling document metadata

    # Custom metadata (user-defined tags, categories, etc.)
    custom_metadata = Column(JSON, nullable=False, default=dict)

    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Soft delete
    is_active = Column(Boolean, default=True, nullable=False)
    archived_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    organization = relationship("OrganizationModel")
    created_by_user = relationship("UserModel")
    chunks = relationship(
        "KnowledgeBaseChunkModel",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    # Indexes and constraints
    __table_args__ = (
        Index("ix_kb_documents_organization_id", "organization_id"),
        Index("ix_kb_documents_uuid", "document_uuid"),
        Index("ix_kb_documents_status", "processing_status"),
        Index("ix_kb_documents_created_at", "created_at"),
    )


class WorkflowRecordingModel(Base):
    """Model for storing audio recordings scoped to an organization.

    Recordings are used in hybrid prompts where parts of the output are pre-recorded
    audio rather than dynamically generated TTS.
    """

    __tablename__ = "workflow_recordings"

    id = Column(Integer, primary_key=True, index=True)

    # Descriptive ID used in prompts (unique per organization)
    recording_id = Column(String(64), nullable=False, index=True)

    # Scoping
    workflow_id = Column(
        Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=True
    )
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # TTS configuration metadata (optional, legacy)
    tts_provider = Column(String, nullable=True)
    tts_model = Column(String, nullable=True)
    tts_voice_id = Column(String, nullable=True)

    # Content
    transcript = Column(Text, nullable=False)

    # Storage
    storage_key = Column(String, nullable=False)
    storage_backend = Column(
        Enum("s3", "minio", name="recording_storage_backend"),
        nullable=False,
        default="s3",
        server_default=text("'s3'::recording_storage_backend"),
    )

    # Extra metadata (file_size_bytes, duration_seconds, original_filename, mime_type, etc.)
    recording_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )

    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Soft delete
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    workflow = relationship("WorkflowModel")
    organization = relationship("OrganizationModel")
    created_by_user = relationship("UserModel")

    # Indexes
    __table_args__ = (
        UniqueConstraint(
            "recording_id",
            "organization_id",
            name="uq_workflow_recordings_recording_id_org",
        ),
        Index("ix_workflow_recordings_workflow_id", "workflow_id"),
        Index("ix_workflow_recordings_org_id", "organization_id"),
        Index("ix_workflow_recordings_recording_id", "recording_id"),
    )


class KnowledgeBaseChunkModel(Base):
    """Model for storing document chunks with vector embeddings.

    Each chunk represents a portion of a document that has been:
    1. Extracted and chunked by docling's HybridChunker
    2. Optionally contextualized with surrounding information
    3. Embedded into a vector representation for semantic search
    """

    __tablename__ = "knowledge_base_chunks"

    id = Column(Integer, primary_key=True, index=True)

    # Link to parent document
    document_id = Column(
        Integer,
        ForeignKey("knowledge_base_documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Organization scoping (denormalized for efficient querying)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Chunk content
    chunk_text = Column(Text, nullable=False)  # The actual chunk text
    contextualized_text = Column(
        Text, nullable=True
    )  # Enriched text from chunker.contextualize()

    # Chunk positioning and metadata
    chunk_index = Column(Integer, nullable=False)  # Position in document (0-based)

    # Docling chunk metadata
    chunk_metadata = Column(
        JSON, nullable=False, default=dict
    )  # Store chunk.meta if available

    # Embedding configuration
    embedding_model = Column(
        String(200), nullable=False
    )  # e.g., "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension = Column(
        Integer, nullable=False
    )  # e.g., 384 for all-MiniLM-L6-v2

    # Vector embedding (pgvector column)
    # The dimension should match the embedding_dimension field
    # Default: 1536 dimensions for OpenAI text-embedding-3-small
    # SentenceTransformer (384-dim) also supported but stored as 384-dim vectors
    embedding = Column(Vector(1536), nullable=True)

    # Token count (useful for chunking strategy analysis)
    token_count = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    document = relationship("KnowledgeBaseDocumentModel", back_populates="chunks")
    organization = relationship("OrganizationModel")

    # Indexes and constraints
    __table_args__ = (
        Index("ix_kb_chunks_document_id", "document_id"),
        Index("ix_kb_chunks_organization_id", "organization_id"),
        Index("ix_kb_chunks_chunk_index", "chunk_index"),
        Index(
            "ix_kb_chunks_embedding_model", "embedding_model"
        ),  # For filtering by model
        # Vector similarity search index (using IVFFlat or HNSW)
        # IVFFlat is good for datasets with 10k-1M vectors
        # HNSW is better for larger datasets but uses more memory
        Index(
            "ix_kb_chunks_embedding_ivfflat",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},  # Adjust based on dataset size
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


class SalesCompanyModel(Base):
    __tablename__ = "sales_companies"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    website = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(64), nullable=True)
    address = Column(Text, nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    category = Column(String(255), nullable=True)
    google_rating = Column(Float, nullable=True)
    source = Column(String(100), nullable=True)
    source_url = Column(String(1000), nullable=True)
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    organization = relationship("OrganizationModel")

    __table_args__ = (
        Index("ix_sales_companies_org_name", "organization_id", "name"),
        Index("ix_sales_companies_org_location", "organization_id", "country", "city"),
        UniqueConstraint(
            "organization_id",
            "name",
            "website",
            name="uq_sales_companies_org_name_website",
        ),
    )


class SalesLeadModel(Base):
    __tablename__ = "sales_leads"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    company_id = Column(
        Integer, ForeignKey("sales_companies.id", ondelete="SET NULL"), nullable=True
    )
    business_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=True)
    phone_number = Column(String(64), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    address = Column(Text, nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    niche = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    keyword = Column(String(255), nullable=True)
    google_rating = Column(Float, nullable=True)
    lead_source = Column(String(100), nullable=True)
    status = Column(String(64), nullable=False, default="new")
    pipeline_stage = Column(String(64), nullable=False, default="new_lead")
    quality_score = Column(Integer, nullable=True)
    qualification_score = Column(Integer, nullable=True)
    classification = Column(String(32), nullable=True)
    timezone = Column(String(64), nullable=True)
    enrichment_status = Column(String(32), nullable=False, default="pending")
    research_status = Column(String(32), nullable=False, default="pending")
    next_action = Column(String(64), nullable=True)
    last_contacted_at = Column(DateTime(timezone=True), nullable=True)
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    archived_at = Column(DateTime(timezone=True), nullable=True)

    organization = relationship("OrganizationModel")
    company = relationship("SalesCompanyModel")
    created_by_user = relationship("UserModel")

    __table_args__ = (
        Index("ix_sales_leads_org_stage", "organization_id", "pipeline_stage"),
        Index("ix_sales_leads_org_status", "organization_id", "status"),
        Index("ix_sales_leads_org_location", "organization_id", "country", "city"),
        Index("ix_sales_leads_org_niche", "organization_id", "niche"),
        Index("ix_sales_leads_phone", "phone_number"),
        Index("ix_sales_leads_email", "email"),
    )


class SalesContactModel(Base):
    __tablename__ = "sales_contacts"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    company_id = Column(
        Integer, ForeignKey("sales_companies.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(64), nullable=True)
    social_url = Column(String(500), nullable=True)
    is_primary = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    company = relationship("SalesCompanyModel")

    __table_args__ = (
        Index("ix_sales_contacts_org_lead", "organization_id", "lead_id"),
        Index("ix_sales_contacts_email", "email"),
    )


class SalesPipelineStageModel(Base):
    __tablename__ = "sales_pipeline_stages"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    key = Column(String(64), nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    is_closed = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_won = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")

    __table_args__ = (
        UniqueConstraint(
            "organization_id", "key", name="uq_sales_pipeline_stage_org_key"
        ),
        Index("ix_sales_pipeline_stages_org_position", "organization_id", "position"),
    )


class SalesCampaignLeadModel(Base):
    __tablename__ = "sales_campaign_leads"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    state = Column(String(32), nullable=False, default="queued")
    attempt_count = Column(Integer, nullable=False, default=0, server_default=text("0"))
    next_attempt_at = Column(DateTime(timezone=True), nullable=True)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    campaign = relationship("CampaignModel")
    lead = relationship("SalesLeadModel")

    __table_args__ = (
        UniqueConstraint(
            "campaign_id", "lead_id", name="uq_sales_campaign_leads_campaign_lead"
        ),
        Index("ix_sales_campaign_leads_org_state", "organization_id", "state"),
        Index("ix_sales_campaign_leads_next_attempt", "next_attempt_at"),
    )


class SalesCallModel(Base):
    __tablename__ = "sales_calls"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="SET NULL"), nullable=True
    )
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True
    )
    workflow_run_id = Column(
        Integer, ForeignKey("workflow_runs.id", ondelete="SET NULL"), nullable=True
    )
    external_call_id = Column(String(255), nullable=True)
    phone_number = Column(String(64), nullable=True)
    direction = Column(String(32), nullable=False, default="outbound")
    status = Column(String(64), nullable=False, default="created")
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    recording_url = Column(String(1000), nullable=True)
    cost_info = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    campaign = relationship("CampaignModel")
    workflow_run = relationship("WorkflowRunModel")

    __table_args__ = (
        Index("ix_sales_calls_org_created", "organization_id", "created_at"),
        Index("ix_sales_calls_lead", "lead_id"),
        Index("ix_sales_calls_campaign", "campaign_id"),
        Index("ix_sales_calls_workflow_run", "workflow_run_id"),
    )


class SalesCallTranscriptModel(Base):
    __tablename__ = "sales_call_transcripts"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    call_id = Column(
        Integer, ForeignKey("sales_calls.id", ondelete="CASCADE"), nullable=False
    )
    transcript_text = Column(Text, nullable=False)
    segments = Column(JSON, nullable=False, default=list, server_default=text("'[]'::json"))
    language = Column(String(32), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    call = relationship("SalesCallModel")

    __table_args__ = (
        UniqueConstraint("call_id", name="uq_sales_call_transcripts_call"),
        Index("ix_sales_call_transcripts_org", "organization_id"),
    )


class SalesCallInsightModel(Base):
    __tablename__ = "sales_call_insights"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    call_id = Column(
        Integer, ForeignKey("sales_calls.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="SET NULL"), nullable=True
    )
    summary = Column(Text, nullable=True)
    sentiment = Column(String(32), nullable=True)
    buying_signals = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    objections = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    qualification = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    qualification_score = Column(Integer, nullable=True)
    recommended_next_action = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    call = relationship("SalesCallModel")
    lead = relationship("SalesLeadModel")

    __table_args__ = (
        UniqueConstraint("call_id", name="uq_sales_call_insights_call"),
        Index(
            "ix_sales_call_insights_org_score",
            "organization_id",
            "qualification_score",
        ),
    )


class SalesActivityModel(Base):
    __tablename__ = "sales_activities"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    actor_type = Column(String(32), nullable=False, default="agent")
    actor_id = Column(String(255), nullable=True)
    activity_type = Column(String(64), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")

    __table_args__ = (
        Index(
            "ix_sales_activities_org_lead_created",
            "organization_id",
            "lead_id",
            "created_at",
        ),
    )


class SalesMeetingModel(Base):
    __tablename__ = "sales_meetings"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    call_id = Column(
        Integer, ForeignKey("sales_calls.id", ondelete="SET NULL"), nullable=True
    )
    title = Column(String(255), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    meeting_url = Column(String(1000), nullable=True)
    status = Column(String(32), nullable=False, default="scheduled")
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    call = relationship("SalesCallModel")

    __table_args__ = (
        Index("ix_sales_meetings_org_scheduled", "organization_id", "scheduled_at"),
        Index("ix_sales_meetings_lead", "lead_id"),
    )


class SalesFollowUpModel(Base):
    __tablename__ = "sales_follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    call_id = Column(
        Integer, ForeignKey("sales_calls.id", ondelete="SET NULL"), nullable=True
    )
    channel = Column(String(32), nullable=False, default="email")
    status = Column(String(32), nullable=False, default="scheduled")
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    subject = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    call = relationship("SalesCallModel")

    __table_args__ = (
        Index(
            "ix_sales_followups_org_status_scheduled",
            "organization_id",
            "status",
            "scheduled_at",
        ),
        Index("ix_sales_followups_lead", "lead_id"),
    )


class SalesResearchReportModel(Base):
    __tablename__ = "sales_research_reports"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="CASCADE"), nullable=False
    )
    company_id = Column(
        Integer, ForeignKey("sales_companies.id", ondelete="SET NULL"), nullable=True
    )
    company_summary = Column(Text, nullable=True)
    pain_points = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    opportunities = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    opening_lines = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    pitch_suggestions = Column(
        JSON, nullable=False, default=list, server_default=text("'[]'::json")
    )
    sources = Column(JSON, nullable=False, default=list, server_default=text("'[]'::json"))
    raw_report = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_by_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    company = relationship("SalesCompanyModel")

    __table_args__ = (
        Index("ix_sales_research_reports_org_lead", "organization_id", "lead_id"),
        Index("ix_sales_research_reports_created", "created_at"),
    )


class SalesKnowledgeSourceModel(Base):
    __tablename__ = "sales_knowledge_sources"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    knowledge_base_document_id = Column(
        Integer,
        ForeignKey("knowledge_base_documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    name = Column(String(255), nullable=False)
    source_type = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False)
    content = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))
    extra_metadata = Column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    organization = relationship("OrganizationModel")
    knowledge_base_document = relationship("KnowledgeBaseDocumentModel")
    created_by_user = relationship("UserModel")

    __table_args__ = (
        Index(
            "ix_sales_knowledge_sources_org_category", "organization_id", "category"
        ),
        Index("ix_sales_knowledge_sources_org_active", "organization_id", "is_active"),
    )


class SalesAgentRunModel(Base):
    __tablename__ = "sales_agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    agent_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="queued")
    input = Column(JSON, nullable=False, default=dict, server_default=text("'{}'::json"))
    output = Column(JSON, nullable=False, default=dict, server_default=text("'{}'::json"))
    error = Column(Text, nullable=True)
    lead_id = Column(
        Integer, ForeignKey("sales_leads.id", ondelete="SET NULL"), nullable=True
    )
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True
    )
    workflow_run_id = Column(
        Integer, ForeignKey("workflow_runs.id", ondelete="SET NULL"), nullable=True
    )
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    organization = relationship("OrganizationModel")
    lead = relationship("SalesLeadModel")
    campaign = relationship("CampaignModel")
    workflow_run = relationship("WorkflowRunModel")

    __table_args__ = (
        Index(
            "ix_sales_agent_runs_org_agent_created",
            "organization_id",
            "agent_type",
            "created_at",
        ),
        Index("ix_sales_agent_runs_status", "status"),
    )
