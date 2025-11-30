"""
CRM Domain

Complete Customer Relationship Management module.
"""

from .models import Company, Contact, Deal, Activity, CustomField
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
from .router import router
from .router_ext import router_ext
from .router_import import router_import

__all__ = [
    # Models
    "Company",
    "Contact",
    "Deal",
    "Activity",
    "CustomField",
    # Schemas
    "CompanyCreate",
    "CompanyRead",
    "CompanyUpdate",
    "ContactCreate",
    "ContactRead",
    "ContactUpdate",
    "DealCreate",
    "DealRead",
    "DealUpdate",
    "ActivityCreate",
    "ActivityRead",
    # Repositories
    "CompanyRepository",
    "ContactRepository",
    "DealRepository",
    "ActivityRepository",
    "CustomFieldRepository",
    # Services
    "CompanyService",
    "ContactService",
    "DealService",
    "ActivityService",
    "CustomFieldService",
    # Routers
    "router",
    "router_ext",
    "router_import",
]
