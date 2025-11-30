"""
Collaboration Domain - Models

Team, Notification, and Comment models for collaboration features.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
import enum

from core.database import Base


# ============================================================================
# Enums
# ===================================================================


class TeamRole(str, enum.Enum):
    """Team member roles."""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class NotificationType(str, enum.Enum):
    """Notification types."""
    MENTION = "mention"
    COMMENT = "comment"
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    PROJECT_UPDATE = "project_update"
    TEAM_INVITE = "team_invite"
    SYSTEM = "system"


class NotificationChannel(str, enum.Enum):
    """Notification delivery channels."""
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"


# ============================================================================
# Team Models
# ============================================================================

class Team(Base):
    """Team model for collaboration."""
    
    __tablename__ = "teams"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Basic Info
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Settings
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Metadata
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    color: Mapped[Optional[str]] = mapped_column(String(7))  # Hex color
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Members (stored as JSON for simplicity)
    members: Mapped[list[dict]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )  # [{user_id: UUID, role: str, joined_at: datetime}]
    
    # Permissions
    permissions: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Multi-tenant
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    
    # Ownership
    owner_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name={self.name})>"


# ============================================================================
# Notification Models
# ============================================================================

class Notification(Base):
    """Notification model for real-time updates."""
    
    __tablename__ = "notifications"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Type & Content
    type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Recipient
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    
    # Related Entity
    entity_type: Mapped[Optional[str]] = mapped_column(String(50))  # task, project, comment, etc.
    entity_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)  # UUID as string
    
    # Actor (who triggered this notification)
    actor_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"))
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Delivery
    channels: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    delivered_channels: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    
    # Data
    data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Priority
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)  # 1-5
    
    # Multi-tenant
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.type}, user_id={self.user_id})>"


# ============================================================================
# Comment Models
# ============================================================================

class Comment(Base):
    """Comment model for entities."""
    
    __tablename__ = "comments"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_html: Mapped[Optional[str]] = mapped_column(Text)  # Rendered markdown
    
    # Entity this comment belongs to
    entity_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # task, project, deal, etc.
    entity_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)  # UUID as string
    
    # Author
    author_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    
    # Threading
    parent_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("comments.id"),
        index=True,
    )
    
    # Mentions
    mentions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)  # [user_id, ...]
    
    # Reactions
    reactions: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )  # {emoji: [user_id, ...]}
    
    # Metadata
    attachments: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Multi-tenant
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, entity_type={self.entity_type}, author_id={self.author_id})>"
