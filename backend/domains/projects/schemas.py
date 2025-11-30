"""
Project Schemas

Pydantic models for Project and Task validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Project Schemas
# ============================================================================


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: str = Field(default="planning")
    priority: Optional[str] = Field(None)
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    budget: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)
    custom_fields: dict = Field(default_factory=dict)


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed_statuses = ["planning", "active", "on_hold", "completed", "cancelled"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_priorities = ["low", "medium", "high", "critical"]
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return v


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    budget: Optional[float] = Field(None, ge=0)
    progress: Optional[int] = Field(None, ge=0, le=100)
    tags: Optional[list[str]] = None
    custom_fields: Optional[dict] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_statuses = ["planning", "active", "on_hold", "completed", "cancelled"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_priorities = ["low", "medium", "high", "critical"]
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return v


class ProjectRead(ProjectBase):
    """Schema for reading a project."""

    id: UUID
    tenant_id: Optional[UUID]
    owner_id: Optional[UUID]
    progress: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Task Schemas
# ============================================================================


class TaskBase(BaseModel):
    """Base task schema."""

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: str = Field(default="todo")
    priority: str = Field(default="medium")
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)
    custom_fields: dict = Field(default_factory=dict)


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    project_id: UUID
    assignee_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    depends_on: list[str] = Field(default_factory=list)  # UUID as strings

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed_statuses = ["todo", "in_progress", "review", "done", "blocked"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        allowed_priorities = ["low", "medium", "high", "critical"]
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return v


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    tags: Optional[list[str]] = None
    custom_fields: Optional[dict] = None
    depends_on: Optional[list[str]] = None  # UUID as strings

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_statuses = ["todo", "in_progress", "review", "done", "blocked"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_priorities = ["low", "medium", "high", "critical"]
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return v


class TaskRead(TaskBase):
    """Schema for reading a task."""

    id: UUID
    project_id: UUID
    assignee_id: Optional[UUID]
    parent_id: Optional[UUID]
    created_by_id: Optional[UUID]
    actual_hours: Optional[float]
    depends_on: list[str]  # UUIDs as strings
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
