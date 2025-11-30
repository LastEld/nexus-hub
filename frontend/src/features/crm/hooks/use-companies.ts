/**
 * Company API Hooks
 * 
 * React Query hooks for company CRUD operations
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { Company, CompanyFormData, CompaniesResponse } from "@/types/crm";
import { toast } from "sonner";

// Query Keys
export const companyKeys = {
    all: ["companies"] as const,
    lists: () => [...companyKeys.all, "list"] as const,
    list: (filters?: Record<string, any>) => [...companyKeys.lists(), filters] as const,
    details: () => [...companyKeys.all, "detail"] as const,
    detail: (id: string) => [...companyKeys.details(), id] as const,
};

// Fetch all companies
export function useCompanies(filters?: Record<string, any>) {
    return useQuery({
        queryKey: companyKeys.list(filters),
        queryFn: async () => {
            const params = new URLSearchParams(filters as any).toString();
            const endpoint = `/crm/companies${params ? `?${params}` : ""}`;
            return apiClient.get<Company[]>(endpoint);
        },
    });
}

// Fetch single company
export function useCompany(id: string) {
    return useQuery({
        queryKey: companyKeys.detail(id),
        queryFn: () => apiClient.get<Company>(`/crm/companies/${id}`),
        enabled: !!id,
    });
}

// Create company mutation
export function useCreateCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: CompanyFormData) =>
            apiClient.post<Company>("/crm/companies", data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
            toast.success("Company created successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to create company");
        },
    });
}

// Update company mutation
export function useUpdateCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: CompanyFormData }) =>
            apiClient.patch<Company>(`/crm/companies/${id}`, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
            queryClient.invalidateQueries({ queryKey: companyKeys.detail(variables.id) });
            toast.success("Company updated successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to update company");
        },
    });
}

// Delete company mutation
export function useDeleteCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) =>
            apiClient.delete(`/crm/companies/${id}`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
            toast.success("Company deleted successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to delete company");
        },
    });
}

// Export companies (CSV)
export function useExportCompanies() {
    return useMutation({
        mutationFn: async () => {
            const response = await apiClient.get<Blob>("/crm/companies/export");
            // Create download link
            const url = window.URL.createObjectURL(response as any);
            const a = document.createElement("a");
            a.href = url;
            a.download = `companies-${new Date().toISOString()}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            return response;
        },
        onSuccess: () => {
            toast.success("Companies exported successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to export companies");
        },
    });
}

// Import companies (CSV)
export function useImportCompanies() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (file: File) => {
            const formData = new FormData();
            formData.append("file", file);
            return apiClient.post("/crm/companies/import", formData);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: companyKeys.lists() });
            toast.success("Companies imported successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to import companies");
        },
    });
}
