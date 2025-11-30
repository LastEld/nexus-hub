"""
Custom Exception Hierarchy

Application-specific exceptions for better error handling.
"""

from typing import Any, Optional


class NexusHubException(Exception):
    """Base exception for all NexusHub errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(NexusHubException):
    """Authentication failed."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class AuthorizationError(NexusHubException):
    """Authorization failed (insufficient permissions)."""
    
    def __init__(self, message: str = "Insufficient permissions", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class NotFoundError(NexusHubException):
    """Resource not found."""
    
    def __init__(self, resource: str = "Resource", details: Optional[dict[str, Any]] = None):
        message = f"{resource} not found"
        super().__init__(message, status_code=404, details=details)


class ValidationError(NexusHubException):
    """Input validation failed."""
    
    def __init__(self, message: str = "Validation failed", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=422, details=details)


class ConflictError(NexusHubException):
    """Resource conflict (e.g., duplicate)."""
    
    def __init__(self, message: str = "Resource conflict", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class RateLimitError(NexusHubException):
    """Rate limit exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=429, details=details)


class ExternalServiceError(NexusHubException):
    """External service error (AI, email, etc.)."""
    
    def __init__(self, service: str, message: str, details: Optional[dict[str, Any]] = None):
        full_message = f"{service} service error: {message}"
        super().__init__(full_message, status_code=503, details=details)


class TenantError(NexusHubException):
    """Tenant-related error."""
    
    def __init__(self, message: str = "Tenant error", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class DatabaseError(NexusHubException):
    """Database operation error."""
    
    def __init__(self, message: str = "Database error", details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


# Alias for consistency
ForbiddenError = AuthorizationError

