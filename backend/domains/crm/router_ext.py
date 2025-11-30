"""
Additional CRM Router Endpoints

Extended API endpoints for winning/losing deals, entity-specific endpoints.
"""

from typing import Annotated, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from .dependencies import (
    get_deal_service,
    get_activity_service,
    get_current_tenant_id,
)
from .service import DealService, ActivityService
from .schemas import DealRead, ActivityRead

router_ext = APIRouter(prefix="/crm", tags=["CRM Extended"])


# ============================================================================
# Extended Deal Endpoints
# ============================================================================


@router_ext.post("/deals/{deal_id}/win", response_model=DealRead)
async def mark_deal_won(
    deal_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
    reason: Optional[str] = None,
):
    """Mark deal as won with optional reason."""
    return await service.move_deal(deal_id, "closed_won", tenant_id, reason)


@router_ext.post("/deals/{deal_id}/lose", response_model=DealRead)
async def mark_deal_lost(
    deal_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
    reason: Optional[str] = None,
):
    """Mark deal as lost with optional reason."""
    return await service.move_deal(deal_id, "closed_lost", tenant_id, reason)


# ============================================================================
# Entity-Specific Activity Endpoints
# ============================================================================


@router_ext.get("/companies/{company_id}/activities", response_model=list[ActivityRead])
async def get_company_activities(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    limit: int = 100,
):
    """Get activities for a specific company."""
    return await service.get_timeline(tenant_id, "company", company_id, limit)


@router_ext.get("/contacts/{contact_id}/activities", response_model=list[ActivityRead])
async def get_contact_activities(
    contact_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    limit: int = 100,
):
    """Get activities for a specific contact."""
    return await service.get_timeline(tenant_id, "contact", contact_id, limit)


@router_ext.get("/deals/{deal_id}/activities", response_model=list[ActivityRead])
async def get_deal_activities(
    deal_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    limit: int = 100,
):
    """Get activities for a specific deal."""
    return await service.get_timeline(tenant_id, "deal", deal_id, limit)
