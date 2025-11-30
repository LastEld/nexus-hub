"""
Enhanced CRM Repository Layer

Complete repository implementation with all queries.
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import BaseRepository
from .models import Company, Contact, Deal, Activity, CustomField


class CompanyRepository(BaseRepository[Company]):
    """Repository for Company entities with enhanced queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)

    async def get_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        status: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
       include_deleted: bool = False,
    ) -> List[Company]:
        """Get companies with filters."""
        query = select(Company).where(Company.tenant_id == tenant_id)

        if not include_deleted:
            query = query.where(Company.deleted_at.is_(None))
        
        if search:
            query = query.where(
                or_(
                    Company.name.ilike(f"%{search}%"),
                    Company.legal_name.ilike(f"%{search}%"),
                    Company.email.ilike(f"%{search}%"),
                )
            )
        
        if industry:
            query = query.where(Company.industry == industry)
        
        if status:
            query = query.where(Company.status == status)
        
        if owner_id:
            query = query.where(Company.owner_id == owner_id)
        
        if tags:
            # PostgreSQL array overlap
            query = query.where(Company.tags.overlap(tags))

        query = query.offset(skip).limit(limit).order_by(Company.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_subsidiaries(self, parent_id: UUID) -> List[Company]:
        """Get all subsidiaries of a company."""
        query = (
            select(Company)
            .where(Company.parent_company_id == parent_id)
            .where(Company.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        status: Optional[str] = None,
    ) -> int:
        """Count companies."""
        query = select(func.count(Company.id)).where(
            Company.tenant_id == tenant_id,
            Company.deleted_at.is_(None),
        )
        
        if status:
            query = query.where(Company.status == status)
        
        result = await self.db.execute(query)
        return result.scalar_one()


class ContactRepository(BaseRepository[Contact]):
    """Repository for Contact entities with enhanced queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(Contact, db)

    async def get_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        company_id: Optional[UUID] = None,
        status: Optional[str] = None,
        lead_status: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        include_deleted: bool = False,
    ) -> List[Contact]:
        """Get contacts with filters."""
        query = select(Contact).where(Contact.tenant_id == tenant_id)

        if not include_deleted:
            query = query.where(Contact.deleted_at.is_(None))
        
        if search:
            query = query.where(
                or_(
                    Contact.full_name.ilike(f"%{search}%"),
                    Contact.email.ilike(f"%{search}%"),
                    Contact.phone.ilike(f"%{search}%"),
                )
            )
        
        if company_id:
            query = query.where(Contact.company_id == company_id)
        
        if status:
            query = query.where(Contact.status == status)
        
        if lead_status:
            query = query.where(Contact.lead_status == lead_status)
        
        if owner_id:
            query = query.where(Contact.owner_id == owner_id)
        
        if tags:
            query = query.where(Contact.tags.overlap(tags))

        query = query.offset(skip).limit(limit).order_by(Contact.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_email(
        self,
        email: str,
        tenant_id: UUID,
    ) -> Optional[Contact]:
        """Get contact by email."""
        query = (
            select(Contact)
            .where(Contact.email == email)
            .where(Contact.tenant_id == tenant_id)
            .where(Contact.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_duplicates(
        self,
        tenant_id: UUID,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> List[Contact]:
        """Find potential duplicate contacts."""
        query = select(Contact).where(
            Contact.tenant_id == tenant_id,
            Contact.deleted_at.is_(None),
        )
        
        if email and phone:
            query = query.where(
                or_(
                    Contact.email == email,
                    Contact.phone == phone,
                )
            )
        elif email:
            query = query.where(Contact.email == email)
        elif phone:
            query = query.where(Contact.phone == phone)
        else:
            return []
        
        result = await self.db.execute(query)
        return list(result.scalars().all())


class DealRepository(BaseRepository[Deal]):
    """Repository for Deal entities with enhanced queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(Deal, db)

    async def get_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        stage: Optional[str] = None,
        status: Optional[str] = None,
        owner_id: Optional[UUID] = None,
        company_id: Optional[UUID] = None,
       include_deleted: bool = False,
    ) -> List[Deal]:
        """Get deals with filters."""
        query = select(Deal).where(Deal.tenant_id == tenant_id)

        if not include_deleted:
            query = query.where(Deal.deleted_at.is_(None))
        
        if search:
            query = query.where(Deal.name.ilike(f"%{search}%"))
        
        if stage:
            query = query.where(Deal.stage == stage)
        
        if status:
            query = query.where(Deal.status == status)
        
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
        
        if company_id:
            query = query.where(Deal.company_id == company_id)

        query = query.offset(skip).limit(limit).order_by(Deal.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_pipeline_summary(
        self,
        tenant_id: UUID,
    ) -> dict:
        """Get deal pipeline summary by stage."""
        query = (
            select(
                Deal.stage,
                func.count(Deal.id).label("count"),
                func.sum(Deal.value).label("total_value"),
                func.avg(Deal.probability).label("avg_probability"),
                func.sum(Deal.expected_revenue).label("total_expected"),
            )
            .where(Deal.tenant_id == tenant_id)
            .where(Deal.deleted_at.is_(None))
            .where(Deal.status == "open")
            .group_by(Deal.stage)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return {
            row.stage: {
                "count": row.count,
                "total_value": float(row.total_value or 0),
                "avg_probability": float(row.avg_probability or 0),
                "total_expected": float(row.total_expected or 0),
            }
            for row in rows
        }

    async def get_forecast(
        self,
        tenant_id: UUID,
        owner_id: Optional[UUID] = None,
    ) -> dict:
        """Get revenue forecast."""
        query = (
            select(
                func.sum(Deal.expected_revenue).label("total_forecast"),
                func.count(Deal.id).label("deal_count"),
            )
            .where(Deal.tenant_id == tenant_id)
            .where(Deal.deleted_at.is_(None))
            .where(Deal.status == "open")
        )
        
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
        
        result = await self.db.execute(query)
        row = result.one()
        
        return {
            "total_forecast": float(row.total_forecast or 0),
            "deal_count": row.deal_count,
        }


class ActivityRepository(BaseRepository[Activity]):
    """Repository for Activity entities."""

    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def get_timeline(
        self,
        tenant_id: UUID,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        limit: int = 100,
    ) -> List[Activity]:
        """Get activity timeline."""
        query = select(Activity).where(Activity.tenant_id == tenant_id)
        
        if entity_type == "company" and entity_id:
            query = query.where(Activity.company_id == entity_id)
        elif entity_type == "contact" and entity_id:
            query = query.where(Activity.contact_id == entity_id)
        elif entity_type == "deal" and entity_id:
            query = query.where(Activity.deal_id == entity_id)
        
        query = query.order_by(Activity.activity_date.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class CustomFieldRepository(BaseRepository[CustomField]):
    """Repository for CustomField entities."""

    def __init__(self, db: AsyncSession):
        super().__init__(CustomField, db)

    async def get_by_entity_type(
        self,
        tenant_id: UUID,
        entity_type: str,
        is_active: bool = True,
    ) -> List[CustomField]:
        """Get custom fields for an entity type."""
        query = (
            select(CustomField)
            .where(CustomField.tenant_id == tenant_id)
            .where(CustomField.entity_type == entity_type)
        )
        
        if is_active:
            query = query.where(CustomField.is_active == True)
        
        query = query.order_by(CustomField.position)
        result = await self.db.execute(query)
        return list(result.scalars().all())
