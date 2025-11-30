"""
Exception handlers for FastAPI.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .errors import NexusHubException


async def nexushub_exception_handler(
    request: Request, exc: NexusHubException
) -> JSONResponse:
    """Handle NexusHub custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "detail": str(exc) if exc else None,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(NexusHubException, nexushub_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
