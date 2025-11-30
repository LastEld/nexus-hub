"""
Identity Domain - Service Layer

Business logic for authentication and user management.
"""

from datetime import datetime, timedelta
from typing import Optional

from core.exceptions import AuthenticationError, NotFoundError
from core.security import create_access_token, create_refresh_token, hash_password, verify_password

from .models import User
from .repository import UserRepository
from .schemas import LoginRequest, TokenResponse, UserCreate, UserRead, UserUpdate


class IdentityService:
    """Service for identity and authentication operations."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user
        """
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create user
        user = await self.repository.create_user(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash,
            full_name=user_data.full_name,
            roles=user_data.roles,
        )
        
        return user
    
    async def authenticate(self, credentials: LoginRequest) -> TokenResponse:
        """
        Authenticate user and generate tokens.
        
        Args:
            credentials: Login credentials
            
        Returns:
            Token response with access and refresh tokens
            
        Raises:
            AuthenticationError: If credentials are invalid
        """
        # Find user by email or username
        user = await self.repository.get_by_email_or_username(credentials.username)
        
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        # Update last login
        await self.repository.update_last_login(user.id)
        
        # Generate tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "roles": user.roles,
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead.model_validate(user),
        )
    
    async def get_user(self, user_id: int) -> User:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User
            
        Raises:
            NotFoundError: If user not found
        """
        user = await self.repository.get(user_id)
        if not user:
            raise NotFoundError("User")
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return await self.repository.get_by_email(email)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Update user information.
        
        Args:
            user_id: User ID
            user_data: Update data
            
        Returns:
            Updated user
        """
        user = await self.get_user(user_id)
        return await self.repository.update(user, user_data.model_dump(exclude_unset=True))
    
    async def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ) -> User:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            Updated user
            
        Raises:
            AuthenticationError: If current password is invalid
        """
        user = await self.get_user(user_id)
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise AuthenticationError("Invalid current password")
        
        # Hash new password
        new_hash = hash_password(new_password)
        
        # Update password
        return await self.repository.update_password(user_id, new_hash)
    
    async def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        tenant_id: Optional[int] = None,
    ) -> list[User]:
        """List users with pagination."""
        if tenant_id:
            return await self.repository.get_by_tenant(tenant_id, skip, limit)
        return await self.repository.get_multi(skip=skip, limit=limit)
    
    async def verify_email(self, token: str) -> User:
        """
        Verify user email with token.
        
        Args:
            token: Verification token
            
        Returns:
            Verified user
            
        Raises:
            NotFoundError: If token is invalid
        """
        # In a real implementation, you would validate the token
        # and find the user by the token
        # For now, this is a placeholder
        raise NotImplementedError("Email verification not implemented")
