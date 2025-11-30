"""
Projects Repository Layer

Handles database operations for Project and Task entities.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import BaseRepository
from .models import Project, Task


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project entities."""

    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)

    async def get_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[Project]:
        """Get all projects for a tenant."""
        query = select(Project).where(Project.tenant_id == tenant_id)

        if not include_deleted:
            query = query.where(Project.deleted_at.is_(None))

        query = query.offset(skip).limit(limit).order_by(Project.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_owner(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:
        """Get projects owned by a user."""
        query = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .where(Project.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Project.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_status(
        self,
        tenant_id: UUID,
        status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:
        """Get projects by status."""
        query = (
            select(Project)
            .where(Project.tenant_id == tenant_id)
            .where(Project.status == status)
            .where(Project.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Project.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entities."""

    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def get_by_project(
        self,
        project_id: UUID,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[Task]:
        """Get all tasks for a project."""
        query = select(Task).where(Task.project_id == project_id)

        if not include_deleted:
            query = query.where(Task.deleted_at.is_(None))

        query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_assignee(
        self,
        assignee_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks assigned to a user."""
        query = (
            select(Task)
            .where(Task.assignee_id == assignee_id)
            .where(Task.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Task.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_status(
        self,
        project_id: UUID,
        status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks by status within a project."""
        query = (
            select(Task)
            .where(Task.project_id == project_id)
            .where(Task.status == status)
            .where(Task.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Task.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_subtasks(
        self,
        parent_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get subtasks of a task."""
        query = (
            select(Task)
            .where(Task.parent_id == parent_id)
            .where(Task.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Task.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
