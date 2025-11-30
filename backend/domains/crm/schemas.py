"""
Enhanced CRM Schemas

Pydantic models for CRM validation with all fields.
"""

from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, EmailStr


# ============================================================================
# Company Schemas
# ============================================================================


class CompanyBase(BaseModel):
    """Base company schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    legal_name: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = None  # prospect, customer, partner, competitor
    status: str = Field(default="active")
    
    # Contact Information
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    fax: Optional[str] = Field(None, max_length=50)
    
    # Address
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(default="US", max_length=2)
    
    # Business Details
    description: Optional[str] = None
    annual_revenue: Optional[Decimal] = Field(None, ge=0)
    employee_count: Optional[int] = Field(None, ge=0)
    fiscal_year_end: Optional[str] = Field(None, max_length=10)
    
    # Social Media
    twitter_handle: Optional[str] = Field(None, max_length=100)
    facebook_url: Optional[str] = Field(None, max_length=500)
    
    # Custom Fields
    custom_fields: dict = Field(default_factory=dict)
    
    # Tags
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = Field(None, max_length=100)
    
    # Metadata
    logo_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    
    parent_company_id: Optional[UUID] = None
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed =["active", "inactive", "lost"]
        if v not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(allowed)}")
        return v


class CompanyUpdate(BaseModel):
    """Schema for updating a company."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    legal_name: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = None
    status: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=2)
    description: Optional[str] = None
    annual_revenue: Optional[Decimal] = Field(None, ge=0)
    employee_count: Optional[int] = Field(None, ge=0)
    custom_fields: Optional[dict] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    parent_company_id: Optional[UUID] = None


class CompanyRead(CompanyBase):
    """Schema for reading a company."""
    
    id: UUID
    tenant_id: UUID
    owner_id: UUID
    parent_company_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Contact Schemas
# ============================================================================


class ContactBase(BaseModel):
    """Base contact schema."""
    
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    prefix: Optional[str] = Field(None, max_length=20)
    suffix: Optional[str] = Field(None, max_length=20)
    
    # Professional
    title: Optional[str] = Field(None, max_length=200)
    department: Optional[str] = Field(None, max_length=100)
    company_id: Optional[UUID] = None
    
    # Contact Details
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=500)
    
    # Address
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=2)
    
    # Social
    linkedin_url: Optional[str] = Field(None, max_length=500)
    twitter_handle: Optional[str] = Field(None, max_length=100)
    
    # Professional Details
    status: str = Field(default="active")
    lead_status: Optional[str] = None
    lead_source: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    
    # Personal
    birthday: Optional[date] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    notes: Optional[str] = None
    
    # Custom Fields
    custom_fields: dict = Field(default_factory=dict)
    
    # Tags
    tags: List[str] = Field(default_factory=list)


class ContactCreate(ContactBase):
    """Schema for creating a contact."""
    
    reports_to_id: Optional[UUID] = None


class ContactUpdate(BaseModel):
    """Schema for updating a contact."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=200)
    department: Optional[str] = Field(None, max_length=100)
    company_id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = None
    lead_status: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    custom_fields: Optional[dict] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class ContactRead(ContactBase):
    """Schema for reading a contact."""
    
    id: UUID
    tenant_id: UUID
    owner_id: UUID
    full_name: str
    reports_to_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Deal Schemas  
# ============================================================================


class DealBase(BaseModel):
    """Base deal schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    company_id: UUID
    contact_id: Optional[UUID] = None
    
    # Pipeline & Stage
    stage: str = Field(...)
    probability: int = Field(default=0, ge=0, le=100)
    
    # Financial
    value: Decimal = Field(..., ge=0)
    currency: str = Field(default="USD", max_length=3)
    
    # Dates
    expected_close_date: Optional[date] = None
    
    # Source & Type
    source: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, max_length=100)
    
    # Custom Fields
    custom_fields: dict = Field(default_factory=dict)
    
    # Tags
    tags: List[str] = Field(default_factory=list)
    
    # Metadata
    notes: Optional[str] = None
    next_step: Optional[str] = Field(None, max_length=255)
    next_step_date: Optional[date] = None


class DealCreate(DealBase):
    """Schema for creating a deal."""
    
    @field_validator("stage")
    @classmethod
    def validate_stage(cls, v: str) -> str:
        allowed = ["prospecting", "qualification", "proposal", "negotiation", "closed_won", "closed_lost"]
        if v not in allowed:
            raise ValueError(f"Stage must be one of: {', '.join(allowed)}")
        return v


class DealUpdate(BaseModel):
    """Schema for updating a deal."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    contact_id: Optional[UUID] = None
    stage: Optional[str] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    value: Optional[Decimal] = Field(None, ge=0)
    expected_close_date: Optional[date] = None
    status: Optional[str] = None
    lost_reason: Optional[str] = None
    win_reason: Optional[str] = None
    custom_fields: Optional[dict] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    next_step: Optional[str] = None
    next_step_date: Optional[date] = None


class DealRead(DealBase):
    """Schema for reading a deal."""
    
    id: UUID
    tenant_id: UUID
    owner_id: UUID
    status: str
    expected_revenue: Optional[Decimal]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Activity Schemas
# ============================================================================


class ActivityBase(BaseModel):
    """Base activity schema."""
    
    type: str = Field(...)  # call, email, meeting, note
    category: Optional[str] = None  # inbound, outbound
    subject: str = Field(..., max_length=500)
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    
    # Relationships
    company_id: Optional[UUID] = None
    contact_id: Optional[UUID] = None
    deal_id: Optional[UUID] = None
    
    # Status & Outcome
    status: str = Field(default="completed")
    outcome: Optional[str] = None
    
    # Dates
    activity_date: datetime


class ActivityCreate(ActivityBase):
    """Schema for creating an activity."""
    pass


class ActivityRead(ActivityBase):
    """Schema for reading an activity."""
    
    id: UUID
    tenant_id: UUID
    user_id: UUID
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
