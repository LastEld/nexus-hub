"""
Collaboration Domain - Pydantic Schemas

Request/Response schemas for Teams, Notifications, and Comments.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================================
# Team Schemas
# ============================================================================

class TeamBase(BaseModel):
    """Base team schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_private: bool = False
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    tags: list[str] = Field(default_factory=list)


class TeamCreate(TeamBase):
    """Schema for creating a team."""
    pass


class TeamUpdate(BaseModel):
    """Schema for updating a team."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_private: Optional[bool] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9AFa-f]{6}$')
    tags: Optional[list[str]] = None
    settings: Optional[dict] = None


class TeamRead(TeamBase):
    """Schema for reading a team."""
    id: UUID
    owner_id: Optional[UUID]
    tenant_id: Optional[UUID]
    is_default: bool
    members: list[dict]
    permissions: dict
    avatar_url: Optional[str]
    settings: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TeamMemberAdd(BaseModel):
    """Schema for adding a team member."""
    user_id: UUID
    role: str = Field(default="member")  # owner, admin, member, viewer


class TeamMemberUpdate(BaseModel):
    """Schema for updating a team member."""
    role: str


# ============================================================================
# Notification Schemas
# ============================================================================

class NotificationBase(BaseModel):
    """Base notification schema."""
    type: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    message: str
    priority: int = Field(default=3, ge=1, le=5)


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    user_id: UUID
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    actor_id: Optional[UUID] = None
    channels: list[str] = Field(default_factory=lambda: ["in_app"])
    data: dict = Field(default_factory=dict)


class NotificationRead(NotificationBase):
    """Schema for reading a notification."""
    id: UUID
    user_id: UUID
    entity_type: Optional[str]
    entity_id: Optional[str]
    actor_id: Optional[UUID]
    is_read: bool
    read_at: Optional[datetime]
    channels: list[str]
    delivered_channels: list[str]
    data: dict
    tenant_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationPreferences(BaseModel):
    """Notification preferences schema."""
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    mention_notifications: bool = True
    task_notifications: bool = True
    comment_notifications: bool = True


# ============================================================================
# Comment Schemas
# ============================================================================

class CommentBase(BaseModel):
    """Base comment schema."""
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    """Schema for creating a comment."""
    entity_type: str = Field(..., min_length=1, max_length=50)
    entity_id: str = Field(..., min_length=1)
    parent_id: Optional[UUID] = None
    mentions: list[str] = Field(default_factory=list)
    attachments: list[dict] = Field(default_factory=list)


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: str = Field(..., min_length=1)


class CommentRead(CommentBase):
    """Schema for reading a comment."""
    id: UUID
    entity_type: str
    entity_id: str
    author_id: UUID
    parent_id: Optional[UUID]
    mentions: list[str]
    reactions: dict
    attachments: list[dict]
    content_html: Optional[str]
    is_edited: bool
    edited_at: Optional[datetime]
    tenant_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReactionAdd(BaseModel):
    """Schema for adding a reaction."""
    emoji: str = Field(..., min_length=1, max_length=10)
