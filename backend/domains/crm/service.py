"""
Enhanced CRM Service Layer

Complete business logic for CRM operations.
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from core.exceptions import NotFoundError, ValidationError, ForbiddenError
from .models import Company, Contact, Deal, Activity, CustomField
from .repository import (
    CompanyRepository,
    ContactRepository,
    DealRepository,
    ActivityRepository,
    CustomFieldRepository,
)
from .schemas import (
    CompanyCreate,
    CompanyUpdate,
    ContactCreate,
    ContactUpdate,
    DealCreate,
    DealUpdate,
    ActivityCreate,
)


class CompanyService:
    """Service for Company business logic."""

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    async def create_company(
        self,
        data: CompanyCreate,
        tenant_id: UUID,
        owner_id: UUID,
        created_by_id: UUID,
    ) -> Company:
        """Create a new company."""
        # Verify parent company if provided
        if data.parent_company_id:
            parent = await self.repository.get(data.parent_company_id)
            if not parent or parent.tenant_id != tenant_id:
                raise ValidationError("Invalid parent company")

        company_dict = data.model_dump()
        company = Company(
            **company_dict,
            tenant_id=tenant_id,
            owner_id=owner_id,
            created_by_id=created_by_id,
        )
        return await self.repository.create(company)

    async def get_company(
        self,
        company_id: UUID,
        tenant_id: UUID,
    ) -> Company:
        """Get company by ID."""
        company = await self.repository.get(company_id)
        if not company or company.tenant_id != tenant_id:
            raise NotFoundError("Company not found")
        return company

    async def update_company(
        self,
        company_id: UUID,
        data: CompanyUpdate,
        tenant_id: UUID,
        updated_by_id: UUID,
    ) -> Company:
        """Update company."""
        company = await self.get_company(company_id, tenant_id)
        
        # Verify parent company if changed
        if data.parent_company_id and data.parent_company_id != company.parent_company_id:
            # Prevent circular reference
            if data.parent_company_id == company.id:
                raise ValidationError("Company cannot be its own parent")
            
            parent = await self.repository.get(data.parent_company_id)
            if not parent or parent.tenant_id != tenant_id:
                raise ValidationError("Invalid parent company")
        
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by_id"] = updated_by_id
        update_data["version"] = company.version + 1
        
        return await self.repository.update(company, update_data)

    async def delete_company(
        self,
        company_id: UUID,
        tenant_id: UUID,
    ) -> Company:
        """Soft delete company."""
        company = await self.get_company(company_id, tenant_id)
        return await self.repository.soft_delete(company)

    async def list_companies(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        **filters,
    ) -> List[Company]:
        """List companies with filters."""
        return await self.repository.get_by_tenant(tenant_id, skip, limit, **filters)

    async def get_company_hierarchy(
        self,
        company_id: UUID,
        tenant_id: UUID,
    ) -> dict:
        """Get company hierarchy (parent and subsidiaries)."""
        company = await self.get_company(company_id, tenant_id)
        
        parent = None
        if company.parent_company_id:
            parent = await self.repository.get(company.parent_company_id)
        
        subsidiaries = await self.repository.get_subsidiaries(company_id)
        
        return {
            "company": company,
            "parent": parent,
            "subsidiaries": subsidiaries,
        }

    async def get_stats(
        self,
        tenant_id: UUID,
    ) -> dict:
        """Get company statistics."""
        total = await self.repository.count_by_tenant(tenant_id)
        active = await self.repository.count_by_tenant(tenant_id, status="active")
        inactive = await self.repository.count_by_tenant(tenant_id, status="inactive")
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "lost": total - active - inactive,
        }


class ContactService:
    """Service for Contact business logic."""

    def __init__(
        self,
        repository: ContactRepository,
        company_repository: CompanyRepository,
    ):
        self.repository = repository
        self.company_repository = company_repository

    async def create_contact(
        self,
        data: ContactCreate,
        tenant_id: UUID,
        owner_id: UUID,
        created_by_id: UUID,
    ) -> Contact:
        """Create a new contact."""
        # Verify company if provided
        if data.company_id:
            company = await self.company_repository.get(data.company_id)
            if not company or company.tenant_id != tenant_id:
                raise ValidationError("Invalid company")

        # Check for duplicate email
        if data.email:
            existing = await self.repository.get_by_email(data.email, tenant_id)
            if existing:
                raise ValidationError("Contact with this email already exists")

        # Verify reports_to if provided
        if data.reports_to_id:
            reports_to = await self.repository.get(data.reports_to_id)
            if not reports_to or reports_to.tenant_id != tenant_id:
                raise ValidationError("Invalid reports_to contact")

        contact_dict = data.model_dump()
        contact = Contact(
            **contact_dict,
            tenant_id=tenant_id,
            owner_id=owner_id,
            created_by_id=created_by_id,
        )
        return await self.repository.create(contact)

    async def get_contact(
        self,
        contact_id: UUID,
        tenant_id: UUID,
    ) -> Contact:
        """Get contact by ID."""
        contact = await self.repository.get(contact_id)
        if not contact or contact.tenant_id != tenant_id:
            raise NotFoundError("Contact not found")
        return contact

    async def update_contact(
        self,
        contact_id: UUID,
        data: ContactUpdate,
        tenant_id: UUID,
        updated_by_id: UUID,
    ) -> Contact:
        """Update contact."""
        contact = await self.get_contact(contact_id, tenant_id)

        # Verify company if changed
        if data.company_id and data.company_id != contact.company_id:
            company = await self.company_repository.get(data.company_id)
            if not company or company.tenant_id != tenant_id:
                raise ValidationError("Invalid company")

        # Check email uniqueness if changed
        if data.email and data.email != contact.email:
            existing = await self.repository.get_by_email(data.email, tenant_id)
            if existing:
                raise ValidationError("Contact with this email already exists")

        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by_id"] = updated_by_id
        update_data["version"] = contact.version + 1
        
        # Update full_name if name fields changed
        if any(k in update_data for k in ["first_name", "last_name", "middle_name", "prefix", "suffix"]):
            parts = []
            if update_data.get("prefix") or contact.prefix:
                parts.append(update_data.get("prefix", contact.prefix))
            if update_data.get("first_name") or contact.first_name:
                parts.append(update_data.get("first_name", contact.first_name))
            if update_data.get("middle_name") or contact.middle_name:
                parts.append(update_data.get("middle_name", contact.middle_name))
            if update_data.get("last_name") or contact.last_name:
                parts.append(update_data.get("last_name", contact.last_name))
            if update_data.get("suffix") or contact.suffix:
                parts.append(update_data.get("suffix", contact.suffix))
            update_data["full_name"] = " ".join(filter(None, parts))

        return await self.repository.update(contact, update_data)

    async def delete_contact(
        self,
        contact_id: UUID,
        tenant_id: UUID,
    ) -> Contact:
        """Soft delete contact."""
        contact = await self.get_contact(contact_id, tenant_id)
        return await self.repository.soft_delete(contact)

    async def list_contacts(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        **filters,
    ) -> List[Contact]:
        """List contacts with filters."""
        return await self.repository.get_by_tenant(tenant_id, skip, limit, **filters)

    async def find_duplicates(
        self,
        tenant_id: UUID,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> List[Contact]:
        """Find duplicate contacts."""
        return await self.repository.find_duplicates(tenant_id, email, phone)


class DealService:
    """Service for Deal business logic."""

    def __init__(
        self,
        repository: DealRepository,
        company_repository: CompanyRepository,
        contact_repository: ContactRepository,
    ):
        self.repository = repository
        self.company_repository = company_repository
        self.contact_repository = contact_repository

    async def create_deal(
        self,
        data: DealCreate,
        tenant_id: UUID,
        owner_id: UUID,
        created_by_id: UUID,
    ) -> Deal:
        """Create a new deal."""
        # Verify company
        company = await self.company_repository.get(data.company_id)
        if not company or company.tenant_id != tenant_id:
            raise ValidationError("Invalid company")

        # Verify contact if provided
        if data.contact_id:
            contact = await self.contact_repository.get(data.contact_id)
            if not contact or contact.tenant_id != tenant_id:
                raise ValidationError("Invalid contact")

        deal_dict = data.model_dump()
        deal = Deal(
            **deal_dict,
            tenant_id=tenant_id,
            owner_id=owner_id,
            created_by_id=created_by_id,
        )
        return await self.repository.create(deal)

    async def get_deal(
        self,
        deal_id: UUID,
        tenant_id: UUID,
    ) -> Deal:
        """Get deal by ID."""
        deal = await self.repository.get(deal_id)
        if not deal or deal.tenant_id != tenant_id:
            raise NotFoundError("Deal not found")
        return deal

    async def update_deal(
        self,
        deal_id: UUID,
        data: DealUpdate,
        tenant_id: UUID,
        updated_by_id: UUID,
    ) -> Deal:
        """Update deal."""
        deal = await self.get_deal(deal_id, tenant_id)

        # Verify contact if changed
        if data.contact_id and data.contact_id != deal.contact_id:
            contact = await self.contact_repository.get(data.contact_id)
            if not contact or contact.tenant_id != tenant_id:
                raise ValidationError("Invalid contact")

        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by_id"] = updated_by_id
        update_data["version"] = deal.version + 1
        
        # Track stage changes
        if "stage" in update_data and update_data["stage"] != deal.stage:
            update_data["stage_changed_at"] = datetime.utcnow()
        
        # Recalculate expected revenue if value or probability changed
        if "value" in update_data or "probability" in update_data:
            value = update_data.get("value", deal.value)
            probability = update_data.get("probability", deal.probability)
            update_data["expected_revenue"] = value * Decimal(probability) / Decimal(100)

        return await self.repository.update(deal, update_data)

    async def move_deal(
        self,
        deal_id: UUID,
        stage: str,
        tenant_id: UUID,
        reason: Optional[str] = None,
    ) -> Deal:
        """Move deal to a new stage."""
        deal = await self.get_deal(deal_id, tenant_id)
        
        update_data = {
            "stage": stage,
            "stage_changed_at": datetime.utcnow(),
        }
        
        # Auto-update status based on stage
        if stage == "closed_won":
            update_data["status"] = "won"
            update_data["actual_close_date"] = datetime.utcnow().date()
            if reason:
                update_data["win_reason"] = reason
        elif stage == "closed_lost":
            update_data["status"] = "lost"
            update_data["actual_close_date"] = datetime.utcnow().date()
            if reason:
                update_data["lost_reason"] = reason
        
        return await self.repository.update(deal, update_data)

    async def delete_deal(
        self,
        deal_id: UUID,
        tenant_id: UUID,
    ) -> Deal:
        """Soft delete deal."""
        deal = await self.get_deal(deal_id, tenant_id)
        return await self.repository.soft_delete(deal)

    async def list_deals(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        **filters,
    ) -> List[Deal]:
        """List deals with filters."""
        return await self.repository.get_by_tenant(tenant_id, skip, limit, **filters)

    async def get_pipeline_summary(
        self,
        tenant_id: UUID,
    ) -> dict:
        """Get pipeline summary."""
        return await self.repository.get_pipeline_summary(tenant_id)

    async def get_forecast(
        self,
        tenant_id: UUID,
        owner_id: Optional[UUID] = None,
    ) -> dict:
        """Get revenue forecast."""
        return await self.repository.get_forecast(tenant_id, owner_id)


class ActivityService:
    """Service for Activity business logic."""

    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    async def create_activity(
        self,
        data: ActivityCreate,
        tenant_id: UUID,
        user_id: UUID,
    ) -> Activity:
        """Create a new activity."""
        activity_dict = data.model_dump()
        activity = Activity(
            **activity_dict,
            tenant_id=tenant_id,
            user_id=user_id,
            created_by_id=user_id,
        )
        
        if activity.status == "completed" and not activity.completed_at:
            activity.completed_at = datetime.utcnow()
        
        return await self.repository.create(activity)

    async def get_timeline(
        self,
        tenant_id: UUID,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        limit: int = 100,
    ) -> List[Activity]:
        """Get activity timeline."""
        return await self.repository.get_timeline(tenant_id, entity_type, entity_id, limit)


class CustomFieldService:
    """Service for CustomField business logic."""

    def __init__(self, repository: CustomFieldRepository):
        self.repository = repository

    async def get_fields_for_entity(
        self,
        tenant_id: UUID,
        entity_type: str,
    ) -> List[CustomField]:
        """Get custom fields for an entity type."""
        return await self.repository.get_by_entity_type(tenant_id, entity_type)
