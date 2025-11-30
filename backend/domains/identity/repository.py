"""
Identity Domain - Repository

Data access layer for user operations.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import BaseRepository
from core.exceptions import ConflictError, NotFoundError

from .models import User


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email_or_username(self, identifier: str) -> Optional[User]:
        """Get user by email or username."""
        result = await self.db.execute(
            select(User).where(
                (User.email == identifier) | (User.username == identifier)
            )
        )
        return result.scalar_one_or_none()
    
    async def create_user(
        self,
        email: str,
        username: str,
        password_hash: str,
        **kwargs,
    ) -> User:
        """
        Create a new user.
        
        Args:
            email: User email
            username: Username
            password_hash: Hashed password
            **kwargs: Additional user fields
            
        Returns:
            Created user
            
        Raises:
            ConflictError: If email or username already exists
        """
        # Check for existing email
        existing_email = await self.get_by_email(email)
        if existing_email:
            raise ConflictError("Email already registered")
        
        # Check for existing username
        existing_username = await self.get_by_username(username)
        if existing_username:
            raise ConflictError("Username already taken")
        
        # Create user
        user_data = {
            "email": email,
            "username": username,
            "password_hash": password_hash,
            **kwargs,
        }
        
        return await self.create(user_data)
    
    async def update_password(self, user_id: int, password_hash: str) -> User:
        """Update user password."""
        user = await self.get(user_id)
        if not user:
            raise NotFoundError("User")
        
        user.password_hash = password_hash
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        
        return user
    
    async def update_last_login(self, user_id: int) -> None:
        """Update user's last login timestamp."""
        from datetime import datetime
        
        user = await self.get(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            self.db.add(user)
            await self.db.flush()
    
    async def verify_email(self, user_id: int) -> User:
        """Mark user email as verified."""
        user = await self.get(user_id)
        if not user:
            raise NotFoundError("User")
        
        user.is_email_verified = True
        user.email_verification_token = None
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        
        return user
    
    async def get_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100) -> list[User]:
        """Get users by tenant."""
        result = await self.db.execute(
            select(User)
            .where(User.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
