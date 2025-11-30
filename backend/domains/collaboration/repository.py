"""
Collaboration Domain - Repository Layer

Database operations for Teams, Notifications, and Comments.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import BaseRepository
from .models import Team, Notification, Comment


class TeamRepository(BaseRepository[Team]):
    """Repository for Team entities."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Team, db)
    
    async def get_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Team]:
        """Get all teams for a tenant."""
        query = (
            select(Team)
            .where(Team.tenant_id == tenant_id)
            .where(Team.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .order_by(Team.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_user_teams(
        self,
        user_id: UUID,
        tenant_id: UUID,
    ) -> list[Team]:
        """Get teams a user is a member of."""
        # This requires JSON query - simplified version
        query = (
            select(Team)
            .where(Team.tenant_id == tenant_id)
            .where(Team.is_deleted == False)
            .order_by(Team.created_at.desc())
        )
        result = await self.db.execute(query)
        teams = list(result.scalars().all())
        
        # Filter in Python (in production, use PostgreSQL JSON operators)
        return [
            team for team in teams
            if any(str(user_id) in str(member.get("user_id", "")) for member in team.members)
        ]


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification entities."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Notification, db)
    
    async def get_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False,
    ) -> list[Notification]:
        """Get notifications for a user."""
        query = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .where(Notification.is_deleted == False)
        )
        
        if unread_only:
            query = query.where(Notification.is_read == False)
        
        query = query.offset(skip).limit(limit).order_by(Notification.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def mark_as_read(
        self,
        user_id: UUID,
        notification_ids: list[UUID],
    ) -> int:
        """Mark notifications as read."""
        from datetime import datetime
        
        for notif_id in notification_ids:
            notif = await self.get(notif_id)
            if notif and notif.user_id == user_id:
                notif.is_read = True
                notif.read_at = datetime.utcnow()
                await self.update(notif)
        
        return len(notification_ids)
    
    async def get_unread_count(self, user_id: UUID) -> int:
        """Get count of unread notifications."""
        from sqlalchemy import func
        
        query = select(func.count()).select_from(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_deleted == False,
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0


class CommentRepository(BaseRepository[Comment]):
    """Repository for Comment entities."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Comment, db)
    
    async def get_by_entity(
        self,
        entity_type: str,
        entity_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Comment]:
        """Get comments for an entity."""
        query = (
            select(Comment)
            .where(Comment.entity_type == entity_type)
            .where(Comment.entity_id == entity_id)
            .where(Comment.is_deleted == False)
            .where(Comment.parent_id.is_(None))  # Top-level only
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at.asc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_replies(
        self,
        parent_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Comment]:
        """Get replies to a comment."""
        query = (
            select(Comment)
            .where(Comment.parent_id == parent_id)
            .where(Comment.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at.asc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_author(
        self,
        author_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Comment]:
        """Get comments by author."""
        query = (
            select(Comment)
            .where(Comment.author_id == author_id)
            .where(Comment.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
