/**
 * Auth Types
 * 
 * TypeScript types for authentication.
 */

export interface User {
    id: number;
    email: string;
    username: string;
    full_name: string | null;
    avatar_url: string | null;
    bio: string | null;
    is_active: boolean;
    is_superuser: boolean;
    is_email_verified: boolean;
    roles: string[];
    tenant_id: number | null;
    two_factor_enabled: boolean;
    last_login_at: string | null;
    created_at: string;
    updated_at: string;
}

export interface LoginRequest {
    username: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    user: User;
}

export interface RegisterRequest {
    email: string;
    username: string;
    password: string;
    full_name?: string;
    roles?: string[];
}

export interface PasswordChangeRequest {
    current_password: string;
    new_password: string;
}
