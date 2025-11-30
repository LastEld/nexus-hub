/**
 * CRM API Client
 * 
 * Type-safe API functions for CRM operations
 */

import { apiClient } from "@/lib/api-client";

// Types
export interface Company {
    id: string;
    name: string;
    legal_name?: string;
    industry?: string;
    company_size?: string;
    website?: string;
    email?: string;
    phone?: string;
    address_line1?: string;
    address_line2?: string;
    city?: string;
    state?: string;
    country?: string;
    postal_code?: string;
    type?: string;
    status: string;
    annual_revenue?: number;
    employee_count?: number;
    description?: string;
    tags?: string[];
    created_at: string;
    updated_at: string;
}

export interface Contact {
    id: string;
    first_name: string;
    middle_name?: string;
    last_name: string;
    full_name?: string;
    email: string;
    phone?: string;
    mobile_phone?: string;
    title?: string;
    department?: string;
    company_id?: string;
    company?: Company;
    lead_status?: string;
    lead_source?: string;
    rating?: number;
    address_line1?: string;
    city?: string;
    state?: string;
    country?: string;
    postal_code?: string;
    linkedin_url?: string;
    twitter_url?: string;
    description?: string;
    tags?: string[];
    created_at: string;
    updated_at: string;
}

export interface Deal {
    id: string;
    name: string;
    company_id: string;
    company?: Company;
    contact_id?: string;
    contact?: Contact;
    stage: string;
    value: number;
    currency: string;
    probability: number;
    expected_revenue?: number;
    expected_close_date?: string;
    actual_close_date?: string;
    pipeline?: string;
    type?: string;
    lead_source?: string;
    description?: string;
    next_step?: string;
    tags?: string[];
    status: string;
    created_at: string;
    updated_at: string;
}

export interface Activity {
    id: string;
    subject: string;
    type: string;
    category?: string;
    description?: string;
    due_date?: string;
    completed_at?: string;
    duration_minutes?: number;
    company_id?: string;
    contact_id?: string;
    deal_id?: string;
    status: string;
    outcome?: string;
    created_at: string;
}

export interface PipelineSummary {
    stage: string;
    count: number;
    total_value: number;
    avg_probability: number;
    expected_revenue: number;
}

// API Functions

export const crmApi = {
    // Companies
    companies: {
        list: (params?: {
            search?: string;
            industry?: string;
            status?: string;
            limit?: number;
            offset?: number;
        }) => apiClient.get<Company[]>("/crm/companies", { params }),

        get: (id: string) => apiClient.get<Company>(`/crm/companies/${id}`),

        create: (data: Partial<Company>) =>
            apiClient.post<Company>("/crm/companies", data),

        update: (id: string, data: Partial<Company>) =>
            apiClient.patch<Company>(`/crm/companies/${id}`, data),

        delete: (id: string) => apiClient.delete(`/crm/companies/${id}`),

        stats: () => apiClient.get("/crm/companies/stats"),

        hierarchy: (id: string) => apiClient.get(`/crm/companies/${id}/hierarchy`),

        export: () => apiClient.get("/crm/companies/export", { responseType: "blob" }),

        bulkUpdate: (ids: string[], updates: Partial<Company>) =>
            apiClient.post("/crm/companies/bulk-update", { company_ids: ids, updates }),

        bulkDelete: (ids: string[]) =>
            apiClient.post("/crm/companies/bulk-delete", { company_ids: ids }),
    },

    // Contacts
    contacts: {
        list: (params?: {
            search?: string;
            company_id?: string;
            lead_status?: string;
            limit?: number;
            offset?: number;
        }) => apiClient.get<Contact[]>("/crm/contacts", { params }),

        get: (id: string) => apiClient.get<Contact>(`/crm/contacts/${id}`),

        create: (data: Partial<Contact>) =>
            apiClient.post<Contact>("/crm/contacts", data),

        update: (id: string, data: Partial<Contact>) =>
            apiClient.patch<Contact>(`/crm/contacts/${id}`, data),

        delete: (id: string) => apiClient.delete(`/crm/contacts/${id}`),

        duplicates: () => apiClient.get<Contact[]>("/crm/contacts/duplicates"),

        activities: (id: string) => apiClient.get<Activity[]>(`/crm/contacts/${id}/activities`),

        export: () => apiClient.get("/crm/contacts/export", { responseType: "blob" }),

        bulkUpdate: (ids: string[], updates: Partial<Contact>) =>
            apiClient.post("/crm/contacts/bulk-update", { contact_ids: ids, updates }),

        bulkDelete: (ids: string[]) =>
            apiClient.post("/crm/contacts/bulk-delete", { contact_ids: ids }),
    },

    // Deals
    deals: {
        list: (params?: {
            search?: string;
            stage?: string;
            status?: string;
            company_id?: string;
            limit?: number;
            offset?: number;
        }) => apiClient.get<Deal[]>("/crm/deals", { params }),

        get: (id: string) => apiClient.get<Deal>(`/crm/deals/${id}`),

        create: (data: Partial<Deal>) =>
            apiClient.post<Deal>("/crm/deals", data),

        update: (id: string, data: Partial<Deal>) =>
            apiClient.patch<Deal>(`/crm/deals/${id}`, data),

        delete: (id: string) => apiClient.delete(`/crm/deals/${id}`),

        move: (id: string, stage: string, notes?: string) =>
            apiClient.post<Deal>(`/crm/deals/${id}/move`, { new_stage: stage, notes }),

        win: (id: string, reason?: string) =>
            apiClient.post<Deal>(`/crm/deals/${id}/win`, { reason }),

        lose: (id: string, reason?: string) =>
            apiClient.post<Deal>(`/crm/deals/${id}/lose`, { reason }),

        pipeline: () => apiClient.get<PipelineSummary[]>("/crm/deals/pipeline"),

        forecast: () => apiClient.get("/crm/deals/forecast"),

        activities: (id: string) => apiClient.get<Activity[]>(`/crm/deals/${id}/activities`),

        export: () => apiClient.get("/crm/deals/export", { responseType: "blob" }),
    },

    // Activities
    activities: {
        list: (params?: {
            company_id?: string;
            contact_id?: string;
            deal_id?: string;
            type?: string;
            limit?: number;
        }) => apiClient.get<Activity[]>("/crm/activities", { params }),

        create: (data: Partial<Activity>) =>
            apiClient.post<Activity>("/crm/activities", data),
    },
};
