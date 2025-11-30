"""
Projects API Router

Complete REST API endpoints for Projects and Tasks (30+ endpoints).
Following implementation_plan.md Phase 3.
"""

from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Project, Task
from .repository import ProjectRepository, TaskRepository
from .schemas import ProjectCreate, ProjectRead, ProjectUpdate, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/projects", tags=["Projects"])


# ============================================================================
# Project CRUD Endpoints (7 endpoints)
# ============================================================================

@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new project."""
    repo = ProjectRepository(db)
    project = Project(
        **data.model_dump(exclude_unset=True),
        owner_id=current_user.id,
        tenant_id=current_user.tenant_id,
    )
    created = await repo.create(project)
    await db.commit()
    await db.refresh(created)
    return created


@router.get("", response_model=List[ProjectRead])
async def list_projects(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
):
    """List all projects for the tenant."""
    repo = ProjectRepository(db)
    if status:
        projects = await repo.get_by_status(current_user.tenant_id, status, skip, limit)
    else:
        projects = await repo.get_by_tenant(current_user.tenant_id, skip, limit)
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get project by ID."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update a project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    
    updated = await repo.update(project)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a project (soft delete)."""
    from datetime import datetime
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.is_deleted = True
    project.deleted_at = datetime.utcnow()
    await repo.update(project)
    await db.commit()


@router.post("/{project_id}/archive", response_model=ProjectRead)
async def archive_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Archive a project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = "archived"
    updated = await repo.update(project)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/{project_id}/restore", response_model=ProjectRead)
async def restore_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Restore an archived project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = "active"
    updated = await repo.update(project)
    await db.commit()
    await db.refresh(updated)
    return updated


# ============================================================================
# Project Members Endpoints (3 endpoints)
# ============================================================================

@router.get("/{project_id}/members", response_model=List[dict])
async def get_project_members(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get project team members."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.participants


@router.post("/{project_id}/members", response_model=ProjectRead)
async def add_project_member(
    project_id: UUID,
    member_data: dict,  # {user_id: UUID, name: str, role: str}
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add a member to the project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Add member to participants
    if not project.participants:
        project.participants = []
    project.participants.append(member_data)
    
    updated = await repo.update(project)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_project_member(
    project_id: UUID,
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Remove a member from the project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Remove member from participants
    project.participants = [
        p for p in project.participants if p.get("user_id") != str(user_id)
    ]
    
    await repo.update(project)
    await db.commit()


# ============================================================================
# Project Stats/Gantt/Timeline Endpoints (4 endpoints)
# ============================================================================

@router.get("/{project_id}/stats", response_model=dict)
async def get_project_stats(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get project statistics."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all tasks for the project
    task_repo = TaskRepository(db)
    tasks = await task_repo.get_by_project(project_id)
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == "completed")
    in_progress = sum(1 for t in tasks if t.status == "in_progress")
    todo = sum(1 for t in tasks if t.status == "todo")
    
    return {
        "project_id": str(project_id),
        "total_tasks": total,
        "completed_tasks": completed,
        "in_progress_tasks": in_progress,
        "todo_tasks": todo,
        "completion_percentage": (completed / total * 100) if total > 0 else 0,
    }


@router.get("/{project_id}/tasks", response_model=List[TaskRead])
async def get_project_tasks(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
):
    """Get all tasks for a project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task_repo = TaskRepository(db)
    if status:
        tasks = await task_repo.get_by_status(project_id, status, skip, limit)
    else:
        tasks = await task_repo.get_by_project(project_id, skip, limit)
    return tasks


@router.get("/{project_id}/gantt", response_model=dict)
async def get_project_gantt(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get Gantt chart data for project."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task_repo = TaskRepository(db)
    tasks = await task_repo.get_by_project(project_id, limit=1000)
    
    return {
        "project_id": str(project_id),
        "project_name": project.name,
        "start_date": project.start_date.isoformat() if project.start_date else None,
        "end_date": project.deadline.isoformat() if project.deadline else None,
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "start_date": t.start_date.isoformat() if t.start_date else None,
                "end_date": t.deadline.isoformat() if t.deadline else None,
                "dependencies": t.depends_on,
                "progress": 100 if t.status == "completed" else 50 if t.status == "in_progress" else 0,
            }
            for t in tasks
        ],
    }


@router.get("/{project_id}/timeline", response_model=List[dict])
async def get_project_timeline(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get project timeline/activity history."""
    repo = ProjectRepository(db)
    project = await repo.get(project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # TODO: Implement activity tracking for projects
    # For now, return basic timeline based on tasks
    task_repo = TaskRepository(db)
    tasks = await task_repo.get_by_project(project_id, limit=1000)
    
    timeline = []
    for task in sorted(tasks, key=lambda t: t.created_at):
        timeline.append({
            "event_type": "task_created",
            "timestamp": task.created_at.isoformat(),
            "description": f"Task '{task.title}' created",
            "task_id": str(task.id),
        })
    
    return timeline


# ============================================================================
# Task CRUD Endpoints (10+ endpoints)
# ============================================================================

@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new task."""
    # Verify project exists and user has access
    project_repo = ProjectRepository(db)
    project = await project_repo.get(data.project_id)
    if not project or project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task_repo = TaskRepository(db)
    task = Task(
        **data.model_dump(exclude_unset=True),
        created_by=current_user.id,
        tenant_id=current_user.tenant_id,
    )
    created = await task_repo.create(task)
    await db.commit()
    await db.refresh(created)
    return created


@router.get("/tasks", response_model=List[TaskRead])
async def list_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    project_id: Optional[UUID] = None,
    assignee_id: Optional[UUID] = None,
):
    """List tasks with filters."""
    task_repo = TaskRepository(db)
    if project_id:
        tasks = await task_repo.get_by_project(project_id, skip, limit)
    elif assignee_id:
        tasks = await task_repo.get_by_assignee(assignee_id, skip, limit)
    else:
        # Get all tasks for tenant's projects
        from sqlalchemy import select
        query = select(Task).where(Task.tenant_id == current_user.tenant_id).offset(skip).limit(limit)
        result = await db.execute(query)
        tasks = list(result.scalars().all())
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get task by ID."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update a task."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a task (soft delete)."""
    from datetime import datetime
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_deleted = True
    task.deleted_at = datetime.utcnow()
    await repo.update(task)
    await db.commit()


@router.post("/tasks/{task_id}/assign", response_model=TaskRead)
async def assign_task(
    task_id: UUID,
    assignee_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Assign task to a user."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.assignee_id = assignee_id
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/tasks/{task_id}/move", response_model=TaskRead)
async def move_task(
    task_id: UUID,
    status: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Move task to a new status (Kanban)."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/tasks/{task_id}/start", response_model=TaskRead)
async def start_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Start working on a task."""
    from datetime import datetime
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "in_progress"
    task.started_at = datetime.utcnow()
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/tasks/{task_id}/complete", response_model=TaskRead)
async def complete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Mark task as completed."""
    from datetime import datetime
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/tasks/{task_id}/subtask", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_subtask(
    task_id: UUID,
    data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a subtask under a parent task."""
    # Verify parent task exists
    repo = TaskRepository(db)
    parent_task = await repo.get(task_id)
    if not parent_task or parent_task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Parent task not found")
    
    task = Task(
        **data.model_dump(exclude_unset=True),
        parent_id=task_id,
        created_by=current_user.id,
        tenant_id=current_user.tenant_id,
    )
    created = await repo.create(task)
    await db.commit()
    await db.refresh(created)
    return created


@router.get("/tasks/{task_id}/subtasks", response_model=List[TaskRead])
async def get_subtasks(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get subtasks of a task."""
    repo = TaskRepository(db)
    parent_task = await repo.get(task_id)
    if not parent_task or parent_task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    subtasks = await repo.get_subtasks(task_id)
    return subtasks


# ============================================================================
# Task Dependencies Endpoints (2 endpoints)
# ============================================================================

@router.post("/tasks/{task_id}/dependencies", response_model=TaskRead)
async def add_task_dependency(
    task_id: UUID,
    dependency_id: str,  # UUID as string
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add a dependency to a task."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.depends_on:
        task.depends_on = []
    if dependency_id not in task.depends_on:
        task.depends_on.append(dependency_id)
    
    updated = await repo.update(task)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/tasks/{task_id}/dependencies/{dependency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task_dependency(
    task_id: UUID,
    dependency_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Remove a dependency from a task."""
    repo = TaskRepository(db)
    task = await repo.get(task_id)
    if not task or task.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.depends_on and dependency_id in task.depends_on:
        task.depends_on.remove(dependency_id)
    
    await repo.update(task)
    await db.commit()


# ============================================================================
# My Tasks / Watched Tasks Endpoints (2 endpoints)
# ============================================================================

@router.get("/tasks/my", response_model=List[TaskRead])
async def get_my_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(100, ge=1, le=500),
):
    """Get tasks assigned to me."""
    repo = TaskRepository(db)
    tasks = await repo.get_by_assignee(current_user.id, limit=limit)
    return tasks


@router.get("/tasks/overdue", response_model=List[TaskRead])
async def get_overdue_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get overdue tasks for current user."""
    from datetime import datetime
    repo = TaskRepository(db)
    my_tasks = await repo.get_by_assignee(current_user.id, limit=500)
    
    return [
        t for t in my_tasks
        if t.deadline and t.deadline < datetime.utcnow().date() and t.status != "completed"
    ]
