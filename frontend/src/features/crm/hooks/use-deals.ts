/**
 * Deal API Hooks
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { Deal, DealFormData } from "@/types/crm";
import { toast } from "sonner";

export const dealKeys = {
    all: ["deals"] as const,
    lists: () => [...dealKeys.all, "list"] as const,
    list: (filters?: Record<string, any>) => [...dealKeys.lists(), filters] as const,
    details: () => [...dealKeys.all, "detail"] as const,
    detail: (id: string) => [...dealKeys.details(), id] as const,
};

export function useDeals(filters?: Record<string, any>) {
    return useQuery({
        queryKey: dealKeys.list(filters),
        queryFn: async () => {
            const params = new URLSearchParams(filters as any).toString();
            const endpoint = `/crm/deals${params ? `?${params}` : ""}`;
            return apiClient.get<Deal[]>(endpoint);
        },
    });
}

export function useDeal(id: string) {
    return useQuery({
        queryKey: dealKeys.detail(id),
        queryFn: () => apiClient.get<Deal>(`/crm/deals/${id}`),
        enabled: !!id,
    });
}

export function useCreateDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: DealFormData) =>
            apiClient.post<Deal>("/crm/deals", data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: dealKeys.lists() });
            toast.success("Deal created successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to create deal");
        },
    });
}

export function useUpdateDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: DealFormData }) =>
            apiClient.patch<Deal>(`/crm/deals/${id}`, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: dealKeys.lists() });
            queryClient.invalidateQueries({ queryKey: dealKeys.detail(variables.id) });
            toast.success("Deal updated successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to update deal");
        },
    });
}

export function useDeleteDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) =>
            apiClient.delete(`/crm/deals/${id}`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: dealKeys.lists() });
            toast.success("Deal deleted successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to delete deal");
        },
    });
}

export function useWinDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) =>
            apiClient.post(`/crm/deals/${id}/win`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: dealKeys.lists() });
            toast.success("Deal marked as won!");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to win deal");
        },
    });
}

export function useLoseDeal() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) =>
            apiClient.post(`/crm/deals/${id}/lose`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: dealKeys.lists() });
            toast.success("Deal marked as lost");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to lose deal");
        },
    });
}
