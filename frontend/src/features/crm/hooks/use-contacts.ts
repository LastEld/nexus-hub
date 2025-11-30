/**
 * Contact API Hooks
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { Contact, ContactFormData } from "@/types/crm";
import { toast } from "sonner";

export const contactKeys = {
    all: ["contacts"] as const,
    lists: () => [...contactKeys.all, "list"] as const,
    list: (filters?: Record<string, any>) => [...contactKeys.lists(), filters] as const,
    details: () => [...contactKeys.all, "detail"] as const,
    detail: (id: string) => [...contactKeys.details(), id] as const,
};

export function useContacts(filters?: Record<string, any>) {
    return useQuery({
        queryKey: contactKeys.list(filters),
        queryFn: async () => {
            const params = new URLSearchParams(filters as any).toString();
            const endpoint = `/crm/contacts${params ? `?${params}` : ""}`;
            return apiClient.get<Contact[]>(endpoint);
        },
    });
}

export function useContact(id: string) {
    return useQuery({
        queryKey: contactKeys.detail(id),
        queryFn: () => apiClient.get<Contact>(`/crm/contacts/${id}`),
        enabled: !!id,
    });
}

export function useCreateContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: ContactFormData) =>
            apiClient.post<Contact>("/crm/contacts", data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
            toast.success("Contact created successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to create contact");
        },
    });
}

export function useUpdateContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: ContactFormData }) =>
            apiClient.patch<Contact>(`/crm/contacts/${id}`, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
            queryClient.invalidateQueries({ queryKey: contactKeys.detail(variables.id) });
            toast.success("Contact updated successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to update contact");
        },
    });
}

export function useDeleteContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) =>
            apiClient.delete(`/crm/contacts/${id}`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: contactKeys.lists() });
            toast.success("Contact deleted successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to delete contact");
        },
    });
}
