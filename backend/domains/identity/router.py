"""
Identity Domain - API Router

FastAPI endpoints for authentication and user management.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.exceptions import AuthenticationError, ConflictError, NotFoundError

from .dependencies import get_current_user, get_identity_service
from .models import User
from .schemas import (
    LoginRequest,
    PasswordChangeRequest,
    TokenResponse,
    UserCreate,
    UserRead,
    UserShort,
    UserUpdate,
)
from .service import IdentityService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    service: IdentityService = Depends(get_identity_service),
):
    """Register a new user."""
    user = await service.create_user(user_data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    service: IdentityService =Depends(get_identity_service),
):
    """
    Login and get access/refresh tokens.
    
    Returns tokens in response body and sets httpOnly cookies.
    """
    token_response = await service.authenticate(credentials)
    
    # Create response with cookies
    response = JSONResponse(
        content=token_response.model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )
    
    # Set httpOnly cookies
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=True,  # Enable in production with HTTPS
        samesite="lax",
        max_age=3600,  # 1 hour
    )
    
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=2592000,  # 30 days
    )
    
    return response


@router.post("/logout")
async def logout():
    """Logout and clear cookies."""
    response = JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=status.HTTP_200_OK,
    )
    
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return response


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user information."""
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: IdentityService = Depends(get_identity_service),
):
    """Update current user information."""
    updated_user = await service.update_user(current_user.id, user_data)
    return updated_user


@router.post("/change-password", response_model=UserRead)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    service: IdentityService = Depends(get_identity_service),
):
    """Change current user password."""
    updated_user = await service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password,
    )
    return updated_user


@router.get("/users", response_model=list[UserShort])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: IdentityService = Depends(get_identity_service),
):
    """List all users (admin only)."""
    # TODO: Add admin permission check
    users = await service.list_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: IdentityService = Depends(get_identity_service),
):
    """Get user by ID."""
    user = await service.get_user(user_id)
    return user
