"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/features/auth/store/authStore";
import { apiClient } from "@/lib/api-client";
import { User } from "@/types/auth";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
    const router = useRouter();
    const { user, isAuthenticated, isLoading, setUser, setLoading } = useAuthStore();

    useEffect(() => {
        const checkAuth = async () => {
            try {
                // Try to get current user from backend
                const currentUser = await apiClient.get<User>("/auth/me");
                setUser(currentUser);
            } catch (error) {
                // Not authenticated, redirect to login
                setUser(null);
                router.push("/auth/login");
            } finally {
                setLoading(false);
            }
        };

        if (!isAuthenticated && !isLoading) {
            checkAuth();
        }
    }, [isAuthenticated, isLoading, router, setUser, setLoading]);

    // Show loading state while checking authentication
    if (isLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <div className="text-center">
                    <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary mx-auto"></div>
                    <p className="mt-4 text-sm text-muted-foreground">Loading...</p>
                </div>
            </div>
        );
    }

    // Don't render children until authenticated
    if (!isAuthenticated || !user) {
        return null;
    }

    return <>{children}</>;
}
