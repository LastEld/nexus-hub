/**
 * React Query hooks for CRM operations
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { crmApi, type Company, type Contact, type Deal } from "../api/crmClient";
import { toast } from "sonner";

// Query Keys
export const crmKeys = {
    all: ["crm"] as const,
    companies: () => [...crmKeys.all, "companies"] as const,
    companiesList: (filters?: any) => [...crmKeys.companies(), "list", filters] as const,
    company: (id: string) => [...crmKeys.companies(), id] as const,
    contacts: () => [...crmKeys.all, "contacts"] as const,
    contactsList: (filters?: any) => [...crmKeys.contacts(), "list", filters] as const,
    contact: (id: string) => [...crmKeys.contacts(), id] as const,
    deals: () => [...crmKeys.all, "deals"] as const,
    dealsList: (filters?: any) => [...crmKeys.deals(), "list", filters] as const,
    deal: (id: string) => [...crmKeys.deals(), id] as const,
    pipeline: () => [...crmKeys.deals(), "pipeline"] as const,
};

// Companies
export function useCompanies(filters?: any) {
    return useQuery({
        queryKey: crmKeys.companiesList(filters),
        queryFn: () => crmApi.companies.list(filters),
    });
}

export function useCompany(id: string) {
    return useQuery({
        queryKey: crmKeys.company(id),
        queryFn: () => crmApi.companies.get(id),
        enabled: !!id,
    });
}

export function useCreateCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Company>) => crmApi.companies.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.companies() });
            toast.success("Company created successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to create company");
        },
    });
}

export function useUpdateCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Company> }) =>
            crmApi.companies.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: crmKeys.company(variables.id) });
            queryClient.invalidateQueries({ queryKey: crmKeys.companies() });
            toast.success("Company updated successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to update company");
        },
    });
}

export function useDeleteCompany() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => crmApi.companies.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.companies() });
            toast.success("Company deleted successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to delete company");
        },
    });
}

// Contacts
export function useContacts(filters?: any) {
    return useQuery({
        queryKey: crmKeys.contactsList(filters),
        queryFn: () => crmApi.contacts.list(filters),
    });
}

export function useContact(id: string) {
    return useQuery({
        queryKey: crmKeys.contact(id),
        queryFn: () => crmApi.contacts.get(id),
        enabled: !!id,
    });
}

export function useCreateContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Contact>) => crmApi.contacts.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.contacts() });
            toast.success("Contact created successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to create contact");
        },
    });
}

export function useUpdateContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Contact> }) =>
            crmApi.contacts.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: crmKeys.contact(variables.id) });
            queryClient.invalidateQueries({ queryKey: crmKeys.contacts() });
            toast.success("Contact updated successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to update contact");
        },
    });
}

export function useDeleteContact() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => crmApi.contacts.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.contacts() });
            toast.success("Contact deleted successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to delete contact");
        },
    });
}

// Deals
export function useDeals(filters?: any) {
    return useQuery({
        queryKey: crmKeys.dealsList(filters),
        queryFn: () => crmApi.deals.list(filters),
    });
}

export function useDeal(id: string) {
    return useQuery({
        queryKey: crmKeys.deal(id),
        queryFn: () => crmApi.deals.get(id),
        enabled: !!id,
    });
}

export function useCreateDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Deal>) => crmApi.deals.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.deals() });
            queryClient.invalidateQueries({ queryKey: crmKeys.pipeline() });
            toast.success("Deal created successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to create deal");
        },
    });
}

export function useUpdateDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Deal> }) =>
            crmApi.deals.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: crmKeys.deal(variables.id) });
            queryClient.invalidateQueries({ queryKey: crmKeys.deals() });
            queryClient.invalidateQueries({ queryKey: crmKeys.pipeline() });
            toast.success("Deal updated successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to update deal");
        },
    });
}

export function useMoveDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, stage, notes }: { id: string; stage: string; notes?: string }) =>
            crmApi.deals.move(id, stage, notes),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.deals() });
            queryClient.invalidateQueries({ queryKey: crmKeys.pipeline() });
            toast.success("Deal moved successfully");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to move deal");
        },
    });
}

export function useWinDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, reason }: { id: string; reason?: string }) =>
            crmApi.deals.win(id, reason),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.deals() });
            queryClient.invalidateQueries({ queryKey: crmKeys.pipeline() });
            toast.success("Deal marked as won! 🎉");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to mark deal as won");
        },
    });
}

export function useLoseDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, reason }: { id: string; reason?: string }) =>
            crmApi.deals.lose(id, reason),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: crmKeys.deals() });
            queryClient.invalidateQueries({ queryKey: crmKeys.pipeline() });
            toast.success("Deal marked as lost");
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to mark deal as lost");
        },
    });
}

export function usePipeline() {
    return useQuery({
        queryKey: crmKeys.pipeline(),
        queryFn: () => crmApi.deals.pipeline(),
    });
}
