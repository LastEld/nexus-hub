"""
Project Domain - Models

Project and Task models for Project Management.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Project(Base):
    """Project model."""
    
    __tablename__ = "projects"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Basic Info
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status & Priority
    status: Mapped[str] = mapped_column(
        String(32),
        default="active",
        index=True,
        nullable=False,
    )  # active, completed, archived, on_hold
    priority: Mapped[int] = mapped_column(Integer, default=3, index=True, nullable=False)  # 1-5
    
    # Timeline
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    deadline: Mapped[Optional[date]] = mapped_column(Date, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Team & Ownership
    owner_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    team_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), index=True)
    participants: Mapped[list[dict]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )  # [{user_id, name, role}]
    
    # Hierarchy
    parent_project_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id"),
    )
    
    # Integration
    repository_url: Mapped[Optional[str]] = mapped_column(String(500))
    external_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Customization
    color: Mapped[Optional[str]] = mapped_column(String(7))  # Hex color
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Metadata
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Features
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # AI & Notes
    ai_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Multi-tenant
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    
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
        return f"<Project(id={self.id}, name={self.name}, status={self.status})>"


class Task(Base):
    """Task model."""
    
    __tablename__ = "tasks"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Basic Info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status & Priority
    status: Mapped[str] = mapped_column(
        String(32),
        default="todo",
        index=True,
        nullable=False,
    )  # todo, in_progress, review, done, blocked
    priority: Mapped[int] = mapped_column(Integer, default=3, index=True, nullable=False)  # 1-5
    
    # Timeline
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    deadline: Mapped[Optional[date]] = mapped_column(Date, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Estimation & Tracking
    estimated_hours: Mapped[Optional[int]] = mapped_column(Integer)
    actual_hours: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    project_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    parent_task_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("tasks.id"),
        index=True,
    )
    
    # Assignment
    assignees: Mapped[list[dict]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )  # [{user_id, name}]
    
    # Dependencies (now using UUIDs)
    depends_on: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )  # Task UUIDs this task depends on (stored as strings)
    
    # Integration
    external_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Metadata
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Features
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_milestone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # AI & Notes
    ai_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Multi-tenant
    tenant_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    
    # Audit
    created_by: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"))
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
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
