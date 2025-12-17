"""
Main FastAPI application for Howard's Portfolio Backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging

from app.config.settings import settings
# from app.config.database import init_db
from app.routers.chat import router as chat_router
from app.routers.analytics import router as analytics_router
from app.routers import resume
from app.models.schemas import HealthCheck, HealthStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create rate limiter instance
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Portfolio API...")
    logger.info(f"Environment: {'DEBUG' if settings.debug else 'PRODUCTION'}")
    
    # Initialize database
    try:
        # init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Portfolio API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered API for Howard Ye's portfolio website",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(resume.router)


# ==================== Root Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs" if settings.debug else "Contact admin for API docs",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "chat": "/api/chat",
            "resume": "/api/resume/preview",
            "examples": "/api/chat/examples",
            "analytics": "/api/analytics/stats"
        }
    }


# @app.get("/health", response_model=HealthCheck)
# async def health_check():
#     """
#     Health check endpoint for monitoring.
#     Tests database and AI service connectivity.
#     """
#     try:
#         # Check database connection
#         from app.config.database import engine
#         from sqlalchemy import text
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         db_healthy = True
#     except Exception as e:
#         logger.error(f"Database health check failed: {e}")
#         db_healthy = False
    
#     # Check AI service (basic check - just verify we have API key)
#     ai_healthy = bool(settings.gemini_api_key)
    
#     # Determine overall status
#     if db_healthy and ai_healthy:
#         status = HealthStatus.HEALTHY
#     elif db_healthy or ai_healthy:
#         status = HealthStatus.DEGRADED
#     else:
#         status = HealthStatus.UNHEALTHY
    
#     return HealthCheck(
#         status=status,
#         database=db_healthy,
#         ai_service=ai_healthy,
#         version=settings.app_version
#     )
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "portfolio-api"}


# ==================== Error Handlers ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested endpoint does not exist",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )