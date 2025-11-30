"""
Enhanced CRM API Router

Complete REST API endpoints for CRM operations.
"""

from typing import Annotated, Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status, HTTPException

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from .dependencies import (
    get_company_service,
    get_contact_service,
    get_deal_service,
    get_activity_service,
    get_custom_field_service,
    get_current_tenant_id,
)
from .service import (
    CompanyService,
    ContactService,
    DealService,
    ActivityService,
    CustomFieldService,
)
from .schemas import (
    CompanyCreate,
    CompanyRead,
    CompanyUpdate,
    ContactCreate,
    ContactRead,
    ContactUpdate,
    DealCreate,
    DealRead,
    DealUpdate,
    ActivityCreate,
    ActivityRead,
)

router = APIRouter(prefix="/crm", tags=["CRM"])


# ============================================================================
# Company Endpoints
# ============================================================================


@router.post("/companies", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Create a new company."""
    return await service.create_company(
        data,
        tenant_id=tenant_id,
        owner_id=current_user.id,
        created_by_id=current_user.id,
    )


@router.get("/companies", response_model=List[CompanyRead])
async def list_companies(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    industry: Optional[str] = None,
    status: Optional[str] = None,
    owner_id: Optional[UUID] = None,
    tags: Optional[str] = None,  # Comma-separated tags
):
    """List all companies with filters."""
    filters = {}
    if search:
        filters["search"] = search
    if industry:
        filters["industry"] = industry
    if status:
        filters["status"] = status
    if owner_id:
        filters["owner_id"] = owner_id
    if tags:
        filters["tags"] = tags.split(",")
    
    return await service.list_companies(tenant_id, skip, limit, **filters)


@router.get("/companies/stats", response_model=dict)
async def get_company_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Get company statistics."""
    return await service.get_stats(tenant_id)


@router.get("/companies/{company_id}", response_model=CompanyRead)
async def get_company(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Get company by ID."""
    return await service.get_company(company_id, tenant_id)


@router.patch("/companies/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: UUID,
    data: CompanyUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Update company."""
    return await service.update_company(
        company_id,
        data,
        tenant_id,
        updated_by_id=current_user.id,
    )


@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Delete company (soft delete)."""
    await service.delete_company(company_id, tenant_id)


@router.get("/companies/{company_id}/hierarchy", response_model=dict)
async def get_company_hierarchy(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Get company hierarchy (parent and subsidiaries)."""
    return await service.get_company_hierarchy(company_id, tenant_id)


# ============================================================================
# Contact Endpoints
# ============================================================================


@router.post("/contacts", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(
    data: ContactCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Create a new contact."""
    return await service.create_contact(
        data,
        tenant_id=tenant_id,
        owner_id=current_user.id,
        created_by_id=current_user.id,
    )


@router.get("/contacts", response_model=List[ContactRead])
async def list_contacts(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    company_id: Optional[UUID] = None,
    status: Optional[str] = None,
    lead_status: Optional[str] = None,
    owner_id: Optional[UUID] = None,
    tags: Optional[str] = None,
):
    """List all contacts with filters."""
    filters = {}
    if search:
        filters["search"] = search
    if company_id:
        filters["company_id"] = company_id
    if status:
        filters["status"] = status
    if lead_status:
        filters["lead_status"] = lead_status
    if owner_id:
        filters["owner_id"] = owner_id
    if tags:
        filters["tags"] = tags.split(",")
    
    return await service.list_contacts(tenant_id, skip, limit, **filters)


@router.get("/contacts/duplicates", response_model=List[ContactRead])
async def find_duplicate_contacts(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """Find duplicate contacts by email or phone."""
    return await service.find_duplicates(tenant_id, email, phone)


@router.get("/contacts/{contact_id}", response_model=ContactRead)
async def get_contact(
    contact_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Get contact by ID."""
    return await service.get_contact(contact_id, tenant_id)


@router.patch("/contacts/{contact_id}", response_model=ContactRead)
async def update_contact(
    contact_id: UUID,
    data: ContactUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Update contact."""
    return await service.update_contact(
        contact_id,
        data,
        tenant_id,
        updated_by_id=current_user.id,
    )


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Delete contact (soft delete)."""
    await service.delete_contact(contact_id, tenant_id)


# ============================================================================
# Deal Endpoints (Sales Pipeline)
# ============================================================================


@router.post("/deals", response_model=DealRead, status_code=status.HTTP_201_CREATED)
async def create_deal(
    data: DealCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Create a new deal."""
    return await service.create_deal(
        data,
        tenant_id=tenant_id,
        owner_id=current_user.id,
        created_by_id=current_user.id,
    )


@router.get("/deals", response_model=List[DealRead])
async def list_deals(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    stage: Optional[str] = None,
    status: Optional[str] = None,
    owner_id: Optional[UUID] = None,
    company_id: Optional[UUID] = None,
):
    """List all deals with optional filters."""
    filters = {}
    if search:
        filters["search"] = search
    if stage:
        filters["stage"] = stage
    if status:
        filters["status"] = status
    if owner_id:
        filters["owner_id"] = owner_id
    if company_id:
        filters["company_id"] = company_id
    
    return await service.list_deals(tenant_id, skip, limit, **filters)


@router.get("/deals/pipeline", response_model=dict)
async def get_pipeline_summary(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Get deal pipeline summary by stage."""
    return await service.get_pipeline_summary(tenant_id)


@router.get("/deals/forecast", response_model=dict)
async def get_revenue_forecast(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
    owner_id: Optional[UUID] = None,
):
    """Get revenue forecast."""
    return await service.get_forecast(tenant_id, owner_id)


@router.get("/deals/{deal_id}", response_model=DealRead)
async def get_deal(
    deal_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Get deal by ID."""
    return await service.get_deal(deal_id, tenant_id)


@router.patch("/deals/{deal_id}", response_model=DealRead)
async def update_deal(
    deal_id: UUID,
    data: DealUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Update deal."""
    return await service.update_deal(
        deal_id,
        data,
        tenant_id,
        updated_by_id=current_user.id,
    )


@router.post("/deals/{deal_id}/move", response_model=DealRead)
async def move_deal_stage(
    deal_id: UUID,
    stage: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
    reason: Optional[str] = None,
):
    """Move deal to a new stage."""
    return await service.move_deal(deal_id, stage, tenant_id, reason)


@router.delete("/deals/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    deal_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Delete deal (soft delete)."""
    await service.delete_deal(deal_id, tenant_id)


# ============================================================================
# Activity Endpoints (Timeline)
# ============================================================================


@router.post("/activities", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity(
    data: ActivityCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
):
    """Create a new activity."""
    return await service.create_activity(data, tenant_id, current_user.id)


@router.get("/activities", response_model=List[ActivityRead])
async def get_activity_timeline(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    entity_type: Optional[str] = None,  # company, contact, deal
    entity_id: Optional[UUID] = None,
    limit: int = Query(100, ge=1, le=500),
):
    """Get activity timeline."""
    return await service.get_timeline(tenant_id, entity_type, entity_id, limit)


@router.get("/activities/{activity_id}", response_model=ActivityRead)
async def get_activity(
    activity_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
):
    """Get activity by ID."""
    activity = await service.repository.get(activity_id)
    if not activity or activity.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.patch("/activities/{activity_id}", response_model=ActivityRead)
async def update_activity(
    activity_id: UUID,
    data: dict,  # Using dict for flexible updates
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
):
    """Update activity."""
    activity = await service.repository.get(activity_id)
    if not activity or activity.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Update fields
    for key, value in data.items():
        if hasattr(activity, key):
            setattr(activity, key, value)
    
    return await service.repository.update(activity)


@router.delete("/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
):
    """Delete activity."""
    activity = await service.repository.get(activity_id)
    if not activity or activity.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    await service.repository.delete(activity_id)


@router.get("/activities/upcoming", response_model=List[ActivityRead])
async def get_upcoming_activities(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    days: int = Query(7, ge=1, le=90),
):
    """Get upcoming activities."""
    from datetime import datetime, timedelta
    end_date = datetime.utcnow() + timedelta(days=days)
    
    # Get all activities and filter by date
    activities = await service.repository.get_by_tenant(tenant_id, skip=0, limit=500)
    return [
        a for a in activities
        if a.activity_date and a.activity_date <= end_date and a.status != "completed"
    ]


@router.get("/activities/overdue", response_model=List[ActivityRead])
async def get_overdue_activities(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
):
    """Get overdue activities."""
    from datetime import datetime
    now = datetime.utcnow()
    
    activities = await service.repository.get_by_tenant(tenant_id, skip=0, limit=500)
    return [
        a for a in activities
        if a.activity_date and a.activity_date < now and a.status != "completed"
    ]


@router.get("/activities/my", response_model=List[ActivityRead])
async def get_my_activities(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ActivityService, Depends(get_activity_service)],
    limit: int = Query(100, ge=1, le=500),
):
    """Get my activities (assigned to current user)."""
    activities = await service.repository.get_by_tenant(tenant_id, skip=0, limit=limit)
    return [a for a in activities if a.user_id == current_user.id]


# ============================================================================
# Custom Fields Endpoints
# ============================================================================


@router.get("/custom-fields/{entity_type}", response_model=List[dict])
async def get_custom_fields(
    entity_type: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Get custom fields for an entity type."""
    return await service.get_fields_for_entity(tenant_id, entity_type)


@router.post("/custom-fields", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_custom_field(
    data: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Create a new custom field definition."""
    from domains.crm.models import CustomField
    from datetime import datetime
    
    field = CustomField(
        tenant_id=tenant_id,
        entity_type=data.get("entity_type"),
        field_name=data.get("field_name"),
        field_label=data.get("field_label"),
        field_type=data.get("field_type"),
        is_required=data.get("is_required", False),
        is_active=data.get("is_active", True),
        display_order=data.get("display_order", 0),
        validation_rules=data.get("validation_rules"),
        options=data.get("options"),
        default_value=data.get("default_value"),
        help_text=data.get("help_text"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    created_field = await service.repository.create(field)
    return {
        "id": str(created_field.id),
        "entity_type": created_field.entity_type,
        "field_name": created_field.field_name,
        "field_label": created_field.field_label,
        "field_type": created_field.field_type,
        "is_required": created_field.is_required,
        "is_active": created_field.is_active,
        "display_order": created_field.display_order,
    }


@router.get("/custom-fields/field/{field_id}", response_model=dict)
async def get_custom_field(
    field_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Get a custom field by ID."""
    field = await service.repository.get(field_id)
    if not field or field.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Custom field not found")
    
    return {
        "id": str(field.id),
        "entity_type": field.entity_type,
        "field_name": field.field_name,
        "field_label": field.field_label,
        "field_type": field.field_type,
        "is_required": field.is_required,
        "is_active": field.is_active,
        "display_order": field.display_order,
        "validation_rules": field.validation_rules,
        "options": field.options,
        "default_value": field.default_value,
        "help_text": field.help_text,
    }


@router.patch("/custom-fields/{field_id}", response_model=dict)
async def update_custom_field(
    field_id: UUID,
    data: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Update a custom field definition."""
    from datetime import datetime
    
    field = await service.repository.get(field_id)
    if not field or field.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Custom field not found")
    
    # Update allowed fields
    for key in ["field_label", "is_required", "is_active", "display_order", 
                "validation_rules", "options", "default_value", "help_text"]:
        if key in data:
            setattr(field, key, data[key])
    
    field.updated_at = datetime.utcnow()
    updated_field = await service.repository.update(field)
    
    return {
        "id": str(updated_field.id),
        "entity_type": updated_field.entity_type,
        "field_name": updated_field.field_name,
        "field_label": updated_field.field_label,
        "field_type": updated_field.field_type,
        "is_required": updated_field.is_required,
        "is_active": updated_field.is_active,
        "display_order": updated_field.display_order,
    }


@router.delete("/custom-fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_field(
    field_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Delete a custom field definition."""
    field = await service.repository.get(field_id)
    if not field or field.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Custom field not found")
    await service.repository.delete(field_id)


@router.post("/custom-fields/reorder", response_model=dict)
async def reorder_custom_fields(
    data: dict,  # {"entity_type": "company", "field_ids": ["uuid1", "uuid2", ...]}
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CustomFieldService, Depends(get_custom_field_service)],
):
    """Reorder custom fields for an entity type."""
    from datetime import datetime
    from uuid import UUID as UUIDType
    
    entity_type = data.get("entity_type")
    field_ids = [UUIDType(fid) if isinstance(fid, str) else fid for fid in data.get("field_ids", [])]
    
    # Update display_order for each field
    for index, field_id in enumerate(field_ids):
        field = await service.repository.get(field_id)
        if field and field.tenant_id == tenant_id and field.entity_type == entity_type:
            field.display_order = index
            field.updated_at = datetime.utcnow()
            await service.repository.update(field)
    
    return {"message": f"Reordered {len(field_ids)} fields", "entity_type": entity_type}

