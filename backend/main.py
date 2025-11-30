"""
FastAPI Application Main Module

Application factory with middleware and route registration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from core.config import settings
from core.database import close_db, init_db
from core.exceptions import register_exception_handlers
from domains.identity.router import router as identity_router
from domains.crm.router import router as crm_router
from domains.crm.router_ext import router_ext as crm_router_ext
from domains.crm.router_import import router_import as crm_router_import
from domains.projects.router import router as projects_router
from domains.collaboration.router_teams import router as teams_router
from domains.collaboration.router_notifications import router as notifications_router
from domains.collaboration.router_comments import router as comments_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 NexusHub starting up...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 NexusHub shutting down...")
    await close_db()
    print("✅ Database connections closed")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready modular business platform",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )
    
    # Add middleware
    configure_middleware(app)
    
    # Add exception handlers
    register_exception_handlers(app)
    
    # Add routes
    configure_routes(app)
    
    return app


def configure_middleware(app: FastAPI) -> None:
    """Configure application middleware."""
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    
    # Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Trusted host (production only)
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"],  # Configure with actual domains
        )


def configure_routes(app: FastAPI) -> None:
    """Configure application routes."""
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}
    
    # API routes
    api_router = APIRouter(prefix=settings.API_PREFIX)
    
    # Include domain routers
    api_router.include_router(identity_router)
    api_router.include_router(crm_router)
    api_router.include_router(crm_router_ext)
    api_router.include_router(crm_router_import)
    api_router.include_router(projects_router)  # Projects domain ✅
    api_router.include_router(teams_router)  # Teams ✅
    api_router.include_router(notifications_router)  # Notifications ✅
    api_router.include_router(comments_router)  # Comments ✅
    
    app.include_router(api_router)


# Create application instance
app = create_application()
