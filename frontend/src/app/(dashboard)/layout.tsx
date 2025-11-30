"use client";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { AppSidebar } from "@/components/layout/app-sidebar";
import { AppHeader } from "@/components/layout/app-header";
import { useUIStore } from "@/stores/ui-store";
import { cn } from "@/lib/utils";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { sidebarCollapsed } = useUIStore();

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-background">
                <AppSidebar />
                <div
                    className={cn(
                        "transition-all duration-300",
                        sidebarCollapsed ? "ml-16" : "ml-64"
                    )}
                >
                    <AppHeader />
                    <main className="p-6">{children}</main>
                </div>
            </div>
        </ProtectedRoute>
    );
}

