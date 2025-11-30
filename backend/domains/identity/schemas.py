"""
Identity Domain - Pydantic Schemas

Request and response schemas for identity operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# Base Schemas
class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, max_length=128)
    roles: list[str] = Field(default_factory=lambda: ["user"])
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roles: Optional[list[str]] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Schema for reading user information."""
    
    id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    is_superuser: bool
    is_email_verified: bool
    roles: list[str]
    tenant_id: Optional[int] = None
    two_factor_enabled: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UserShort(BaseModel):
    """Short user schema for listings."""
    
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    
    model_config = {"from_attributes": True}


# Authentication Schemas
class LoginRequest(BaseModel):
    """Login request schema."""
    
    username: str  # Can be username or email
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


class PasswordChangeRequest(BaseModel):
    """Password change request."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class PasswordResetRequest(BaseModel):
    """Password reset initiation."""
    
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""
    
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class EmailVerificationRequest(BaseModel):
    """Email verification request."""
    
    token: str


# 2FA Schemas
class TwoFactorSetupResponse(BaseModel):
    """2FA setup response."""
    
    secret: str
    qr_code: str  # Base64 encoded QR code


class TwoFactorVerifyRequest(BaseModel):
    """2FA verification request."""
    
    code: str = Field(..., min_length=6, max_length=6)


class TwoFactorLoginRequest(LoginRequest):
    """Login with 2FA code."""
    
    code: str = Field(..., min_length=6, max_length=6)
