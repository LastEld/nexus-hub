"""
Identity Domain - Dependencies

Dependency injection for identity services.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.exceptions import AuthenticationError
from core.security import decode_token

from .repository import UserRepository
from .service import IdentityService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Get user repository dependency."""
    return UserRepository(db)


def get_identity_service(
    repository: UserRepository = Depends(get_user_repository),
) -> IdentityService:
    """Get identity service dependency."""
    return IdentityService(repository)


async def get_current_user_id(
    # TODO: Get token from cookie or header
    token: str = "",
) -> int:
    """
    Get current user ID from JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        User ID
        
    Raises:
        AuthenticationError: If token is invalid
    """
    if not token:
        raise AuthenticationError("Not authenticated")
    
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise AuthenticationError("Invalid token payload")
    
    return int(user_id)


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    service: IdentityService = Depends(get_identity_service),
):
    """
    Get current authenticated user.
    
    Args:
        user_id: Current user ID
        service: Identity service
        
    Returns:
        Current user
    """
    return await service.get_user(user_id)


async def get_current_active_user(
    current_user = Depends(get_current_user),
):
    """
    Get current active user (not disabled).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Active user
        
    Raises:
        AuthenticationError: If user is disabled/inactive
    """
    if not current_user:
        raise AuthenticationError("User not found")
    
    # Check if user has is_active attribute and if it's False
    if hasattr(current_user, 'is_active') and not current_user.is_active:
        raise AuthenticationError("User account is disabled")
    
    return current_user

