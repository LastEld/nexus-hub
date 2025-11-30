/**
 * useAuth Hook
 * 
 * React hook for authentication operations.
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { authAPI } from "../api/authClient";
import { useAuthStore } from "../store/authStore";
import { LoginRequest, RegisterRequest, PasswordChangeRequest } from "@/types/auth";

export function useAuth() {
    const router = useRouter();
    const queryClient = useQueryClient();
    const { user, isAuthenticated, setUser, setLoading, logout: logoutStore } = useAuthStore();

    // Fetch current user on mount
    const { data: currentUser, isLoading } = useQuery({
        queryKey: ["currentUser"],
        queryFn: authAPI.getCurrentUser,
        retry: false,
        staleTime: Infinity,
    });

    // Update store when user data changes
    useEffect(() => {
        if (currentUser) {
            setUser(currentUser);
        } else {
            setUser(null);
        }
    }, [currentUser, setUser]);

    // Login mutation
    const loginMutation = useMutation({
        mutationFn: authAPI.login,
        onSuccess: (data) => {
            setUser(data.user);
            queryClient.setQueryData(["currentUser"], data.user);
            toast.success("Login successful!");
            router.push("/dashboard");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Login failed");
        },
    });

    // Register mutation
    const registerMutation = useMutation({
        mutationFn: authAPI.register,
        onSuccess: (user) => {
            toast.success("Registration successful! Please login.");
            router.push("/auth/login");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Registration failed");
        },
    });

    // Logout mutation
    const logoutMutation = useMutation({
        mutationFn: authAPI.logout,
        onSuccess: () => {
            logoutStore();
            queryClient.clear();
            toast.success("Logged out successfully");
            router.push("/auth/login");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Logout failed");
        },
    });

    // Change password mutation
    const changePasswordMutation = useMutation({
        mutationFn: authAPI.changePassword,
        onSuccess: () => {
            toast.success("Password changed successfully");
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to change password");
        },
    });

    return {
        user,
        isAuthenticated,
        isLoading,
        login: (credentials: LoginRequest) => loginMutation.mutate(credentials),
        register: (data: RegisterRequest) => registerMutation.mutate(data),
        logout: () => logoutMutation.mutate(),
        changePassword: (data: PasswordChangeRequest) => changePasswordMutation.mutate(data),
        isLoginLoading: loginMutation.isPending,
        isRegisterLoading: registerMutation.isPending,
        isLogoutLoading: logoutMutation.isPending,
    };
}
