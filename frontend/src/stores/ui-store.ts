/**
 * UI Store
 * 
 * Zustand store for UI state management (sidebar, theme, etc.)
 */

import { create } from "zustand";

interface UIState {
    sidebarCollapsed: boolean;
    activeNavItem: string | null;
    setSidebarCollapsed: (collapsed: boolean) => void;
    toggleSidebar: () => void;
    setActiveNavItem: (item: string | null) => void;
}

export const useUIStore = create<UIState>((set) => ({
    sidebarCollapsed: false,
    activeNavItem: null,

    setSidebarCollapsed: (collapsed: boolean) => set({ sidebarCollapsed: collapsed }),

    toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

    setActiveNavItem: (item: string | null) => set({ activeNavItem: item }),
}));

