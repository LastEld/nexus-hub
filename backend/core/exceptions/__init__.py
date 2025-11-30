"""Exceptions package."""

from .errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DatabaseError,
    ExternalServiceError,
    ForbiddenError,
    NexusHubException,
    NotFoundError,
    RateLimitError,
    TenantError,
    ValidationError,
)
from .handlers import general_exception_handler, nexushub_exception_handler, register_exception_handlers

__all__ = [
    "NexusHubException",
    "AuthenticationError",
    "AuthorizationError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "RateLimitError",
    "ExternalServiceError",
    "TenantError",
    "DatabaseError",
    "nexushub_exception_handler",
    "general_exception_handler",
    "register_exception_handlers",
]
