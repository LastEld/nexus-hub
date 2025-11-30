"""
Import/Export Service for CRM Entities

Handles CSV/Excel import and export for companies, contacts, and deals.
"""

import csv
import io
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from fastapi import UploadFile, HTTPException, status


class ImportExportService:
    """Service for importing and exporting CRM data."""

    # CSV Headers for each entity
    COMPANY_HEADERS = [
        "name", "legal_name", "industry", "company_size", "website",
        "linkedin_url", "email", "phone", "address_line1", "address_line2",
        "city", "state", "country", "postal_code", "type", "status",
        "annual_revenue", "employee_count", "description", "tags"
    ]

    CONTACT_HEADERS = [
        "first_name", "middle_name", "last_name", "email", "phone",
        "mobile", "title", "department", "company_name", "lead_status",
        "lead_source", "rating", "address_line1", "city", "state",
        "country", "postal_code", "linkedin_url", "twitter_url",
        "description", "tags"
    ]

    DEAL_HEADERS = [
        "name", "company_name", "contact_email", "stage", "value",
        "currency", "probability", "expected_close_date", "pipeline",
        "type", "lead_source", "description", "next_step", "tags"
    ]

    @staticmethod
    def export_companies_to_csv(companies: List[Dict[str, Any]]) -> str:
        """
        Export companies to CSV format.
        
        Args:
            companies: List of company dictionaries
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=ImportExportService.COMPANY_HEADERS, extrasaction='ignore')
        
        writer.writeheader()
        for company in companies:
            # Convert tags array to comma-separated string
            if 'tags' in company and isinstance(company['tags'], list):
                company['tags'] = ','.join(company['tags'])
            writer.writerow(company)
        
        return output.getvalue()

    @staticmethod
    def export_contacts_to_csv(contacts: List[Dict[str, Any]]) -> str:
        """
        Export contacts to CSV format.
        
        Args:
            contacts: List of contact dictionaries
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=ImportExportService.CONTACT_HEADERS, extrasaction='ignore')
        
        writer.writeheader()
        for contact in contacts:
            # Convert tags array to comma-separated string
            if 'tags' in contact and isinstance(contact['tags'], list):
                contact['tags'] = ','.join(contact['tags'])
            writer.writerow(contact)
        
        return output.getvalue()

    @staticmethod
    def export_deals_to_csv(deals: List[Dict[str, Any]]) -> str:
        """
        Export deals to CSV format.
        
        Args:
            deals: List of deal dictionaries
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=ImportExportService.DEAL_HEADERS, extrasaction='ignore')
        
        writer.writeheader()
        for deal in deals:
            # Convert tags array to comma-separated string
            if 'tags' in deal and isinstance(deal['tags'], list):
                deal['tags'] = ','.join(deal['tags'])
            # Format dates
            if 'expected_close_date' in deal and isinstance(deal['expected_close_date'], datetime):
                deal['expected_close_date'] = deal['expected_close_date'].isoformat()
            writer.writerow(deal)
        
        return output.getvalue()

    @staticmethod
    async def parse_csv_file(file: UploadFile) -> List[Dict[str, Any]]:
        """
        Parse uploaded CSV file.
        
        Args:
            file: Uploaded CSV file
            
        Returns:
            List of dictionaries representing rows
            
        Raises:
            HTTPException: If file is invalid
        """
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV files are supported"
            )
        
        try:
            content = await file.read()
            decoded = content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return list(reader)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error parsing CSV file: {str(e)}"
            )

    @staticmethod
    def validate_company_import(data: List[Dict[str, Any]]) -> tuple[List[Dict], List[Dict]]:
        """
        Validate company import data.
        
        Returns:
            Tuple of (valid_records, errors)
        """
        valid = []
        errors = []
        
        for idx, row in enumerate(data):
            row_errors = []
            
            # Required fields
            if not row.get('name'):
                row_errors.append("Name is required")
            
            # Email validation (basic)
            if row.get('email') and '@' not in row.get('email', ''):
                row_errors.append("Invalid email format")
            
            if row_errors:
                errors.append({
                    "row": idx + 1,
                    "data": row,
                    "errors": row_errors
                })
            else:
                # Convert tags string back to array
                if 'tags' in row and isinstance(row['tags'], str):
                    row['tags'] = [t.strip() for t in row['tags'].split(',') if t.strip()]
                valid.append(row)
        
        return valid, errors

    @staticmethod
    def validate_contact_import(data: List[Dict[str, Any]]) -> tuple[List[Dict], List[Dict]]:
        """
        Validate contact import data.
        
        Returns:
            Tuple of (valid_records, errors)
        """
        valid = []
        errors = []
        
        for idx, row in enumerate(data):
            row_errors = []
            
            # Required fields
            if not row.get('first_name') or not row.get('last_name'):
                row_errors.append("First name and last name are required")
            
            if not row.get('email'):
                row_errors.append("Email is required")
            elif '@' not in row.get('email', ''):
                row_errors.append("Invalid email format")
            
            if row_errors:
                errors.append({
                    "row": idx + 1,
                    "data": row,
                    "errors": row_errors
                })
            else:
                # Convert tags string back to array
                if 'tags' in row and isinstance(row['tags'], str):
                    row['tags'] = [t.strip() for t in row['tags'].split(',') if t.strip()]
                valid.append(row)
        
        return valid, errors

    @staticmethod
    def validate_deal_import(data: List[Dict[str, Any]]) -> tuple[List[Dict], List[Dict]]:
        """
        Validate deal import data.
        
        Returns:
            Tuple of (valid_records, errors)
        """
        valid = []
        errors = []
        
        for idx, row in enumerate(data):
            row_errors = []
            
            # Required fields
            if not row.get('name'):
                row_errors.append("Deal name is required")
            
            if not row.get('company_name'):
                row_errors.append("Company name is required")
            
            # Value validation
            if row.get('value'):
                try:
                    float(row['value'])
                except ValueError:
                    row_errors.append("Invalid value format")
            
            if row_errors:
                errors.append({
                    "row": idx + 1,
                    "data": row,
                    "errors": row_errors
                })
            else:
                # Convert tags string back to array
                if 'tags' in row and isinstance(row['tags'], str):
                    row['tags'] = [t.strip() for t in row['tags'].split(',') if t.strip()]
                valid.append(row)
        
        return valid, errors
