"""
CRM Dependencies

Dependency injection for CRM domain.
"""

from typing import Annotated
from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from .repository import (
    CompanyRepository,
    ContactRepository,
    DealRepository,
    ActivityRepository,
    CustomFieldRepository,
)
from .service import (
    CompanyService,
    ContactService,
    DealService,
    ActivityService,
    CustomFieldService,
)


# Repository dependencies
def get_company_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> CompanyRepository:
    """Get company repository."""
    return CompanyRepository(db)


def get_contact_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ContactRepository:
    """Get contact repository."""
    return ContactRepository(db)


def get_deal_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> DealRepository:
    """Get deal repository."""
    return DealRepository(db)


def get_activity_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ActivityRepository:
    """Get activity repository."""
    return ActivityRepository(db)


def get_custom_field_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> CustomFieldRepository:
    """Get custom field repository."""
    return CustomFieldRepository(db)


# Service dependencies
def get_company_service(
    repository: Annotated[CompanyRepository, Depends(get_company_repository)]
) -> CompanyService:
    """Get company service."""
    return CompanyService(repository)


def get_contact_service(
    contact_repo: Annotated[ContactRepository, Depends(get_contact_repository)],
    company_repo: Annotated[CompanyRepository, Depends(get_company_repository)],
) -> ContactService:
    """Get contact service."""
    return ContactService(contact_repo, company_repo)


def get_deal_service(
    deal_repo: Annotated[DealRepository, Depends(get_deal_repository)],
    company_repo: Annotated[CompanyRepository, Depends(get_company_repository)],
    contact_repo: Annotated[ContactRepository, Depends(get_contact_repository)],
) -> DealService:
    """Get deal service."""
    return DealService(deal_repo, company_repo, contact_repo)


def get_activity_service(
    repository: Annotated[ActivityRepository, Depends(get_activity_repository)]
) -> ActivityService:
    """Get activity service."""
    return ActivityService(repository)


def get_custom_field_service(
    repository: Annotated[CustomFieldRepository, Depends(get_custom_field_repository)]
) -> CustomFieldService:
    """Get custom field service."""
    return CustomFieldService(repository)


# Helper to get tenant_id from current user
# TODO: Implement proper tenant resolution from user context
async def get_current_tenant_id() -> UUID:
    """Get current tenant ID from user context."""
    # Temporary: return a default tenant ID
    # In production, this should come from the authenticated user
    from uuid import uuid4
    return uuid4()  # Replace with actual tenant resolution
