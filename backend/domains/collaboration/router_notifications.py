"""
Notifications API Router

Notification system endpoints (8+ endpoints).
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Notification
from .repository import NotificationRepository
from .schemas import NotificationCreate, NotificationRead, NotificationPreferences

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification(
    data: NotificationCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a notification."""
    repo = NotificationRepository(db)
    notification = Notification(
        **data.model_dump(),
        tenant_id=current_user.tenant_id,
    )
    created = await repo.create(notification)
    await db.commit()
    await db.refresh(created)
    return created


@router.get("", response_model=List[NotificationRead])
async def list_notifications(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    unread_only: bool = False,
):
    """List notifications for current user."""
    repo = NotificationRepository(db)
    notifications = await repo.get_by_user(current_user.id, skip, limit, unread_only)
    return notifications


@router.get("/unread/count", response_model=dict)
async def get_unread_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get count of unread notifications."""
    repo = NotificationRepository(db)
    count = await repo.get_unread_count(current_user.id)
    return {"count": count}


@router.post("/mark-read", response_model=dict)
async def mark_notifications_read(
    notification_ids: List[UUID],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Mark notifications as read."""
    repo = NotificationRepository(db)
    count = await repo.mark_as_read(current_user.id, notification_ids)
    await db.commit()
    return {"marked": count}


@router.post("/mark-all-read", response_model=dict)
async def mark_all_read(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Mark all notifications as read."""
    repo = NotificationRepository(db)
    notifications = await repo.get_by_user(current_user.id, unread_only=True, limit=1000)
    notification_ids = [n.id for n in notifications]
    count = await repo.mark_as_read(current_user.id, notification_ids)
    await db.commit()
    return {"marked": count}


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a notification."""
    from datetime import datetime
    repo = NotificationRepository(db)
    notification = await repo.get(notification_id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_deleted = True
    notification.deleted_at = datetime.utcnow()
    await repo.update(notification)
    await db.commit()


@router.get("/preferences", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get notification preferences (stub)."""
    # TODO: Implement user preferences storage
    return NotificationPreferences()


@router.patch("/preferences", response_model=NotificationPreferences)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update notification preferences (stub)."""
    # TODO: Implement user preferences storage
    return preferences
