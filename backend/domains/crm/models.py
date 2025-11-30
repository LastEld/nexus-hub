"""
Enhanced CRM Models

Complete CRM entity models with all fields and relationships.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Date, Text, 
    Numeric, ARRAY, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from core.database import Base


class Company(Base):
    """Company entity - Enhanced with full CRM features."""
    
    __tablename__ = "companies"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    legal_name = Column(String(255))
    industry = Column(String(100), index=True)
    company_size = Column(String(50))  # 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+
    website = Column(String(500))
    linkedin_url = Column(String(500))
    type = Column(String(50))  # prospect, customer, partner, competitor
    status = Column(String(50), default="active", index=True)  # active, inactive, lost
    
    # Contact Information
    email = Column(String(255))
    phone = Column(String(50))
    fax = Column(String(50))
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(2), default="US")
    
    # Business Details
    description = Column(Text)
    annual_revenue = Column(Numeric(15, 2))
    employee_count = Column(Integer)
    fiscal_year_end = Column(String(10))
    tax_id = Column(String(100))  # Should be encrypted in production
    
    # Relationships
    parent_company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Social Media
    twitter_handle = Column(String(100))
    facebook_url = Column(String(500))
    
    # Custom Fields
    custom_fields = Column(JSONB, default={})
    
    # Tags & Categories
    tags = Column(ARRAY(String), default=[], index=True)
    source = Column(String(100))  # website, referral, campaign, cold-call
    
    # Metadata
    logo_url = Column(String(500))
    favicon_url = Column(String(500))
    notes = Column(Text)
    company_metadata = Column(JSONB, default={})
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    version = Column(Integer, default=1, nullable=False)
    
    # Relationships
    # tenant = relationship("Tenant", back_populates="companies")
    # owner = relationship("User", foreign_keys=[owner_id])
    parent_company = relationship("Company", remote_side=[id], backref="subsidiaries")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="company", cascade="all, delete-orphan")
    # activities = relationship("Activity", back_populates="company")
    
    __table_args__ = (
        Index("idx_company_tenant_name", "tenant_id", "name"),
        Index("idx_company_tags", "tags", postgresql_using="gin"),
    )


class Contact(Base):
    """Contact entity - Enhanced with full CRM features."""
    
    __tablename__ = "contacts"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Basic Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    prefix = Column(String(20))  # Dr., Mr., Ms., etc.
    suffix = Column(String(20))  # Jr., Sr., III, etc.
    full_name = Column(String(255), nullable=False, index=True)
    
    # Professional
    title = Column(String(200))  # Job title
    department = Column(String(100))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), index=True)
    reports_to_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"))
    
    # Contact Details
    email = Column(String(255), index=True)
    phone = Column(String(50))
    mobile = Column(String(50))
    fax = Column(String(50))
    website = Column(String(500))
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(2))
    
    # Social
    linkedin_url = Column(String(500))
    twitter_handle = Column(String(100))
    facebook_url = Column(String(500))
    
    # Professional Details
    status = Column(String(50), default="active", index=True)  # active, inactive, bounced, unsubscribed
    lead_status = Column(String(50))  # new, contacted, qualified, lost
    lead_source = Column(String(100))  # website, referral, event, advertisement
    rating = Column(Integer)  # 1-5
    do_not_contact = Column(Boolean, default=False)
    email_opt_out = Column(Boolean, default=False)
    
    # Personal
    birthday = Column(Date)
    avatar_url = Column(String(500))
    description = Column(Text)
    notes = Column(Text)
    
    # Custom Fields
    custom_fields = Column(JSONB, default={})
    
    # Tags
    tags = Column(ARRAY(String), default=[], index=True)
    
    # Ownership
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Metadata
    contact_metadata = Column(JSONB, default={})
    last_contacted_at = Column(DateTime)
    contact_count = Column(Integer, default=0)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    version = Column(Integer, default=1, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="contacts")
    # owner = relationship("User", foreign_keys=[owner_id])
    reports_to = relationship("Contact", remote_side=[id], backref="direct_reports")
    deals = relationship("Deal", back_populates="contact")
    # activities = relationship("Activity", back_populates="contact")
    
    __table_args__ = (
        Index("idx_contact_tenant_email", "tenant_id", "email"),
        Index("idx_contact_tags", "tags", postgresql_using="gin"),
        UniqueConstraint("tenant_id", "email", name="uq_contact_tenant_email"),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-generate full_name
        if not self.full_name:
            parts = []
            if self.prefix:
                parts.append(self.prefix)
            if self.first_name:
                parts.append(self.first_name)
            if self.middle_name:
                parts.append(self.middle_name)
            if self.last_name:
                parts.append(self.last_name)
            if self.suffix:
                parts.append(self.suffix)
            self.full_name = " ".join(parts)


class Deal(Base):
    """Deal entity - Sales pipeline."""
    
    __tablename__ = "deals"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Relationships
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Pipeline & Stage
    pipeline_id = Column(UUID(as_uuid=True))  # FK to Pipeline (to be created)
    stage = Column(String(100), nullable=False, index=True)
    stage_changed_at = Column(DateTime, default=datetime.utcnow)
    probability = Column(Integer, default=0)  # 0-100
    
    # Financial
    value = Column(Numeric(15, 2), nullable=False, index=True)
    currency = Column(String(3), default="USD")
    expected_revenue = Column(Numeric(15, 2))  # Calculated: value * probability / 100
    
    # Dates
    expected_close_date = Column(Date, index=True)
    actual_close_date = Column(Date)
    created_date = Column(Date, default=date.today)
    
    # Status
    status = Column(String(50), default="open", index=True)  # open, won, lost, abandoned
    lost_reason = Column(String(255))
    win_reason = Column(String(255))
    
    # Source & Type
    source = Column(String(100))  # inbound, outbound, referral, partner
    type = Column(String(100))  # new_business, upsell, renewal
    
    # Products
    products = Column(JSONB, default=[])  # [{product_id, quantity, price, discount}]
    
    # Custom Fields
    custom_fields = Column(JSONB, default={})
    
    # Tags
    tags = Column(ARRAY(String), default=[], index=True)
    
    # Metadata
    notes = Column(Text)
    deal_metadata = Column(JSONB, default={})
    next_step = Column(String(255))
    next_step_date = Column(Date)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    version = Column(Integer, default=1, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="deals")
    contact = relationship("Contact", back_populates="deals")
    # owner = relationship("User", foreign_keys=[owner_id])
    # activities = relationship("Activity", back_populates="deal")
    
    __table_args__ = (
        Index("idx_deal_tags", "tags", postgresql_using="gin"),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-calculate expected revenue
        if self.value and self.probability is not None:
            self.expected_revenue = self.value * Decimal(self.probability) / Decimal(100)


class Activity(Base):
    """Activity entity - Timeline/History tracking."""
    
    __tablename__ = "activities"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Type & Category
    type = Column(String(50), nullable=False, index=True)
    category = Column(String(50))
    
    # Content
    subject = Column(String(500), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), index=True)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), index=True)
    # task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), index=True)
    
    # Status & Outcome
    status = Column(String(50), default="completed")
    outcome = Column(String(100))
    
    # Dates
    activity_date = Column(DateTime, nullable=False, index=True)
    completed_at = Column(DateTime)
    
    # Metadata
    activity_metadata = Column(JSONB, default={})
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    # user = relationship("User", foreign_keys=[user_id])
    # company = relationship("Company", back_populates="activities")
    # contact = relationship("Contact", back_populates="activities")
    # deal = relationship("Deal", back_populates="activities")


class CustomField(Base):
    """Custom Field definitions for dynamic fields."""
    
    __tablename__ = "custom_fields"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Definition
    entity_type = Column(String(50), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(200), nullable=False)
    field_type = Column(String(50), nullable=False)
    is_required = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)
    
    # Validation
    validation_rules = Column(JSONB, default={})
    options = Column(ARRAY(String))
    default_value = Column(String(255))
    
    # Display
    position = Column(Integer, default=0)
    help_text = Column(Text)
    placeholder = Column(String(255))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "entity_type", "field_name", name="uq_custom_field"),
    )
