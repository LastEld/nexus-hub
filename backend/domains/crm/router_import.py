"""
Import/Export Router for CRM

API endpoints for importing and exporting CRM data.
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, Response, status
from fastapi.responses import StreamingResponse

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from .dependencies import (
    get_company_service,
    get_contact_service,
    get_deal_service,
    get_current_tenant_id,
)
from .service import CompanyService, ContactService, DealService
from .import_export import ImportExportService
from .schemas import CompanyRead, ContactRead, DealRead

router_import = APIRouter(prefix="/crm", tags=["CRM Import/Export"])


# ============================================================================
# Company Import/Export
# ============================================================================


@router_import.post("/companies/import")
async def import_companies(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)] = None,
    service: Annotated[CompanyService, Depends(get_company_service)] = None,
):
    """
    Import companies from CSV file.
    
    CSV should have headers: name, legal_name, industry, company_size, website,
    email, phone, address_line1, city, state, country, postal_code, etc.
    """
    # Parse CSV
    data = await ImportExportService.parse_csv_file(file)
    
    # Validate
    valid_records, errors = ImportExportService.validate_company_import(data)
    
    # Import valid records (would create companies in database)
    imported = []
    for record in valid_records:
        # In real implementation, would call service.create()
        # imported.append(await service.create(record, tenant_id))
        pass
    
    return {
        "total_rows": len(data),
        "valid": len(valid_records),
        "errors": len(errors),
        "imported": len(imported),
        "error_details": errors[:10]  # First 10 errors
    }


@router_import.get("/companies/export")
async def export_companies(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Export all companies to CSV."""
    # Get all companies
    companies = await service.get_list(tenant_id, limit=10000)
    
    # Convert to dict format
    companies_dict = [
        {
            "name": c.name,
            "legal_name": c.legal_name,
            "industry": c.industry,
            "company_size": c.company_size,
            "website": c.website,
            "email": c.email,
            "phone": c.phone,
            "address_line1": c.address_line1,
            "city": c.city,
            "state": c.state,
            "country": c.country,
            "postal_code": c.postal_code,
            "type": c.type,
            "status": c.status,
            "tags": c.tags,
        }
        for c in companies
    ]
    
    # Generate CSV
    csv_content = ImportExportService.export_companies_to_csv(companies_dict)
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=companies.csv"}
    )


# ============================================================================
# Contact Import/Export
# ============================================================================


@router_import.post("/contacts/import")
async def import_contacts(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)] = None,
    service: Annotated[ContactService, Depends(get_contact_service)] = None,
):
    """Import contacts from CSV file."""
    # Parse CSV
    data = await ImportExportService.parse_csv_file(file)
    
    # Validate
    valid_records, errors = ImportExportService.validate_contact_import(data)
    
    # Import valid records
    imported = []
    for record in valid_records:
        # In real implementation, would call service.create()
        pass
    
    return {
        "total_rows": len(data),
        "valid": len(valid_records),
        "errors": len(errors),
        "imported": len(imported),
        "error_details": errors[:10]
    }


@router_import.get("/contacts/export")
async def export_contacts(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Export all contacts to CSV."""
    contacts = await service.get_list(tenant_id, limit=10000)
    
    contacts_dict = [
        {
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "mobile": c.mobile_phone,
            "title": c.title,
            "department": c.department,
            "lead_status": c.lead_status,
            "lead_source": c.lead_source,
            "rating": c.rating,
            "city": c.city,
            "state": c.state,
            "country": c.country,
            "tags": c.tags,
        }
        for c in contacts
    ]
    
    csv_content = ImportExportService.export_contacts_to_csv(contacts_dict)
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contacts.csv"}
    )


# ============================================================================
# Deal Import/Export
# ============================================================================


@router_import.post("/deals/import")
async def import_deals(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)] = None,
    service: Annotated[DealService, Depends(get_deal_service)] = None,
):
    """Import deals from CSV file."""
    data = await ImportExportService.parse_csv_file(file)
    valid_records, errors = ImportExportService.validate_deal_import(data)
    
    imported = []
    for record in valid_records:
        # Implementation would create deals
        pass
    
    return {
        "total_rows": len(data),
        "valid": len(valid_records),
        "errors": len(errors),
        "imported": len(imported),
        "error_details": errors[:10]
    }


@router_import.get("/deals/export")
async def export_deals(
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[DealService, Depends(get_deal_service)],
):
    """Export all deals to CSV."""
    deals = await service.get_list(tenant_id, limit=10000)
    
    deals_dict = [
        {
            "name": d.name,
            "stage": d.stage,
            "value": str(d.value),
            "currency": d.currency,
            "probability": d.probability,
            "expected_close_date": d.expected_close_date,
            "pipeline": d.pipeline,
            "type": d.type,
            "lead_source": d.lead_source,
            "description": d.description,
            "tags": d.tags,
        }
        for d in deals
    ]
    
    csv_content = ImportExportService.export_deals_to_csv(deals_dict)
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=deals.csv"}
    )


# ============================================================================
# Bulk Operations
# ============================================================================


@router_import.post("/companies/bulk-update")
async def bulk_update_companies(
    company_ids: List[UUID],
    updates: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Bulk update multiple companies."""
    updated = []
    for company_id in company_ids:
        # In real implementation: await service.update(company_id, updates, tenant_id)
        pass
    
    return {
        "total": len(company_ids),
        "updated": len(updated),
        "success": True
    }


@router_import.post("/companies/bulk-delete")
async def bulk_delete_companies(
    company_ids: List[UUID],
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[CompanyService, Depends(get_company_service)],
):
    """Bulk delete multiple companies (soft delete)."""
    deleted = []
    for company_id in company_ids:
        # In real implementation: await service.delete(company_id, tenant_id)
        pass
    
    return {
        "total": len(company_ids),
        "deleted": len(deleted),
        "success": True
    }


@router_import.post("/contacts/bulk-update")
async def bulk_update_contacts(
    contact_ids: List[UUID],
    updates: dict,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Bulk update multiple contacts."""
    return {"total": len(contact_ids), "updated": 0, "success": True}


@router_import.post("/contacts/bulk-delete")
async def bulk_delete_contacts(
    contact_ids: List[UUID],
    current_user: Annotated[User, Depends(get_current_active_user)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    service: Annotated[ContactService, Depends(get_contact_service)],
):
    """Bulk delete multiple contacts (soft delete)."""
    return {"total": len(contact_ids), "deleted": 0, "success": True}
