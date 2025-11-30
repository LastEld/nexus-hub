/**
 * Company Types
 */

export interface Company {
    id: string;
    name: string;
    website?: string | null;
    industry?: string | null;
    employee_count?: number | null;
    annual_revenue?: number | null;
    description?: string | null;
    status: "lead" | "customer" | "prospect" | "inactive";
    tags: string[];
    parent_company_id?: string | null;
    address?: string | null;
    city?: string | null;
    state?: string | null;
    country?: string | null;
    postal_code?: string | null;
    phone?: string | null;
    email?: string | null;
    created_at: string;
    updated_at: string;
}

export interface CompanyFormData {
    name: string;
    website?: string;
    industry?: string;
    employee_count?: number;
    annual_revenue?: number;
    description?: string;
    status: "lead" | "customer" | "prospect" | "inactive";
    tags?: string[];
    parent_company_id?: string;
    address?: string;
    city?: string;
    state?: string;
    country?: string;
    postal_code?: string;
    phone?: string;
    email?: string;
}

export interface CompaniesResponse {
    companies: Company[];
    total: number;
    page: number;
    page_size: number;
}

/**
 * Contact Types
 */

export interface Contact {
    id: string;
    first_name: string;
    last_name: string;
    email?: string | null;
    phone?: string | null;
    mobile?: string | null;
    title?: string | null;
    department?: string | null;
    company_id?: string | null;
    status: "active" | "inactive" | "lead";
    tags: string[];
    address?: string | null;
    city?: string | null;
    state?: string | null;
    country?: string | null;
    postal_code?: string | null;
    notes?: string | null;
    created_at: string;
    updated_at: string;
}

export interface ContactFormData {
    first_name: string;
    last_name: string;
    email?: string;
    phone?: string;
    mobile?: string;
    title?: string;
    department?: string;
    company_id?: string;
    status: "active" | "inactive" | "lead";
    tags?: string[];
    address?: string;
    city?: string;
    state?: string;
    country?: string;
    postal_code?: string;
    notes?: string;
}

/**
 * Deal Types
 */

export interface Deal {
    id: string;
    title: string;
    value: number;
    stage: "lead" | "qualified" | "proposal" | "negotiation" | "won" | "lost";
    probability: number;
    expected_close_date?: string | null;
    company_id?: string | null;
    contact_id?: string | null;
    description?: string | null;
    tags: string[];
    created_at: string;
    updated_at: string;
}

export interface DealFormData {
    title: string;
    value: number;
    stage: "lead" | "qualified" | "proposal" | "negotiation" | "won" | "lost";
    probability: number;
    expected_close_date?: string;
    company_id?: string;
    contact_id?: string;
    description?: string;
    tags?: string[];
}

