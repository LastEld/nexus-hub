"""
Teams API Router

Team management endpoints (10+ endpoints).
"""

from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Team
from .repository import TeamRepository
from .schemas import TeamCreate, TeamRead, TeamUpdate, TeamMemberAdd, TeamMemberUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])


# ============================================================================
# Team CRUD Endpoints
# ============================================================================

@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    data: TeamCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new team."""
    repo = TeamRepository(db)
    team = Team(
        **data.model_dump(),
        owner_id=current_user.id,
        tenant_id=current_user.tenant_id,
        members=[{
            "user_id": str(current_user.id),
            "role": "owner",
            "name": current_user.full_name or current_user.username,
            "joined_at": None,
        }],
    )
    created = await repo.create(team)
    await db.commit()
    await db.refresh(created)
    return created


@router.get("", response_model=List[TeamRead])
async def list_teams(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """List all teams for tenant."""
    repo = TeamRepository(db)
    teams = await repo.get_by_tenant(current_user.tenant_id, skip, limit)
    return teams


@router.get("/{team_id}", response_model=TeamRead)
async def get_team(
    team_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get team by ID."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamRead)
async def update_team(
    team_id: UUID,
    data: TeamUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update a team."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(team, key, value)
    
    updated = await repo.update(team)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a team (soft delete)."""
    from datetime import datetime
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team.is_deleted = True
    team.deleted_at = datetime.utcnow()
    await repo.update(team)
    await db.commit()


# ============================================================================
# Team Members Endpoints
# ============================================================================

@router.get("/{team_id}/members", response_model=List[dict])
async def get_team_members(
    team_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get team members."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.members


@router.post("/{team_id}/members", response_model=TeamRead)
async def add_team_member(
    team_id: UUID,
    member: TeamMemberAdd,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add a member to the team."""
    from datetime import datetime
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user already in team
    if any(str(member.user_id) in str(m.get("user_id", "")) for m in team.members):
        raise HTTPException(status_code=400, detail="User already in team")
    
    # Add member
    team.members.append({
        "user_id": str(member.user_id),
        "role": member.role,
        "joined_at": datetime.utcnow().isoformat(),
    })
    
    updated = await repo.update(team)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    team_id: UUID,
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Remove a member from the team."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Remove member
    team.members = [
        m for m in team.members if str(user_id) not in str(m.get("user_id", ""))
    ]
    
    await repo.update(team)
    await db.commit()


@router.patch("/{team_id}/members/{user_id}", response_model=TeamRead)
async def update_team_member_role(
    team_id: UUID,
    user_id: UUID,
    data: TeamMemberUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update team member role."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Update member role
    for member in team.members:
        if str(user_id) in str(member.get("user_id", "")):
            member["role"] = data.role
            break
    else:
        raise HTTPException(status_code=404, detail="Member not found in team")
    
    updated = await repo.update(team)
    await db.commit()
    await db.refresh(updated)
    return updated


# ============================================================================
# Team Permissions & Settings
# ============================================================================

@router.get("/{team_id}/permissions", response_model=dict)
async def get_team_permissions(
    team_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get team permissions."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.permissions or {}


@router.patch("/{team_id}/permissions", response_model=TeamRead)
async def update_team_permissions(
    team_id: UUID,
    permissions: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update team permissions."""
    repo = TeamRepository(db)
    team = await repo.get(team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team.permissions = permissions
    updated = await repo.update(team)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.get("/my/teams", response_model=List[TeamRead])
async def get_my_teams(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get teams I'm a member of."""
    repo = TeamRepository(db)
    teams = await repo.get_user_teams(current_user.id, current_user.tenant_id)
    return teams
