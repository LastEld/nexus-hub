/**
 * Auth API Client
 * 
 * API functions for authentication.
 */

import { apiClient } from "@/lib/api-client";
import {
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    User,
    PasswordChangeRequest,
} from "@/types/auth";

export const authAPI = {
    /**
     * Register a new user
     */
    register: async (data: RegisterRequest): Promise<User> => {
        return apiClient.post<User>("/auth/register", data);
    },

    /**
     * Login with credentials
     */
    login: async (credentials: LoginRequest): Promise<TokenResponse> => {
        return apiClient.post<TokenResponse>("/auth/login", credentials);
    },

    /**
     * Logout
     */
    logout: async (): Promise<{ message: string }> => {
        return apiClient.post("/auth/logout");
    },

    /**
     * Get current user
     */
    getCurrentUser: async (): Promise<User> => {
        return apiClient.get<User>("/auth/me");
    },

    /**
     * Update current user
     */
    updateCurrentUser: async (data: Partial<User>): Promise<User> => {
        return apiClient.patch<User>("/auth/me", data);
    },

    /**
     * Change password
     */
    changePassword: async (data: PasswordChangeRequest): Promise<User> => {
        return apiClient.post<User>("/auth/change-password", data);
    },
};
