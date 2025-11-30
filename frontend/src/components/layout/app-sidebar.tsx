"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useUIStore } from "@/stores/ui-store";
import {
    LayoutDashboard,
    Building2,
    Users,
    Briefcase,
    CheckSquare,
    MessageSquare,
    Bell,
    Settings,
    ChevronLeft,
    ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    {
        name: "CRM", icon: Building2, children: [
            { name: "Companies", href: "/crm/companies" },
            { name: "Contacts", href: "/crm/contacts" },
            { name: "Deals", href: "/crm/deals" },
            { name: "Activities", href: "/crm/activities" },
        ]
    },
    { name: "Projects", href: "/projects", icon: Briefcase },
    { name: "Tasks", href: "/tasks", icon: CheckSquare },
    { name: "Teams", href: "/teams", icon: Users },
    { name: "Settings", href: "/settings", icon: Settings },
];

export function AppSidebar() {
    const pathname = usePathname();
    const { sidebarCollapsed, toggleSidebar } = useUIStore();

    return (
        <aside
            className={cn(
                "fixed left-0 top-0 z-40 h-screen border-r bg-background transition-all duration-300",
                sidebarCollapsed ? "w-16" : "w-64"
            )}
        >
            <div className="flex h-full flex-col">
                {/* Logo */}
                <div className="flex h-16 items-center justify-between border-b px-4">
                    {!sidebarCollapsed && (
                        <Link href="/dashboard" className="flex items-center gap-2">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
                                N
                            </div>
                            <span className="text-lg font-semibold">NexusHub</span>
                        </Link>
                    )}
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={toggleSidebar}
                        className={cn("h-8 w-8", sidebarCollapsed && "mx-auto")}
                    >
                        {sidebarCollapsed ? (
                            <ChevronRight className="h-4 w-4" />
                        ) : (
                            <ChevronLeft className="h-4 w-4" />
                        )}
                    </Button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 space-y-1 overflow-y-auto p-2">
                    {navigation.map((item) => (
                        <div key={item.name}>
                            {item.href ? (
                                <Link
                                    href={item.href}
                                    className={cn(
                                        "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                                        pathname === item.href
                                            ? "bg-primary text-primary-foreground"
                                            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                                        sidebarCollapsed && "justify-center"
                                    )}
                                >
                                    {item.icon && <item.icon className="h-5 w-5 shrink-0" />}
                                    {!sidebarCollapsed && <span>{item.name}</span>}
                                </Link>
                            ) : (
                                <>
                                    <div
                                        className={cn(
                                            "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground",
                                            sidebarCollapsed && "justify-center"
                                        )}
                                    >
                                        {item.icon && <item.icon className="h-5 w-5 shrink-0" />}
                                        {!sidebarCollapsed && <span>{item.name}</span>}
                                    </div>
                                    {!sidebarCollapsed && item.children && (
                                        <div className="ml-4 space-y-1 mt-1">
                                            {item.children.map((child) => (
                                                <Link
                                                    key={child.name}
                                                    href={child.href}
                                                    className={cn(
                                                        "block rounded-lg px-3 py-2 text-sm transition-colors",
                                                        pathname === child.href
                                                            ? "bg-primary/10 text-primary font-medium"
                                                            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                                                    )}
                                                >
                                                    {child.name}
                                                </Link>
                                            ))}
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    ))}
                </nav>
            </div>
        </aside>
    );
}
