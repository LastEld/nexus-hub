"""
Tenant Model

Multi-tenant support for the platform.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB

from core.database import Base


class Tenant(Base):
    """Tenant entity for multi-tenancy."""
    
    __tablename__ = "tenants"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic Information
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    domain = Column(String(255), unique=True)
    
    # Plan & Status
    plan = Column(String(50), default="free")  # free, starter, professional, enterprise
    status = Column(String(50), default="active")  # active, suspended, cancelled
    
    # Settings
    settings = Column(JSONB, default={})
    
    # Limits
    max_users = Column(Integer)
    max_storage_mb = Column(Integer)
    
    # Features
    features = Column(ARRAY(String), default=[])
    
    # Metadata
    tenant_metadata = Column(JSONB, default={})
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    trial_ends_at = Column(DateTime)
    subscription_ends_at = Column(DateTime)
