"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, users, body, products, brands, recommendations, admin, analytics

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered body-aware style recommendations API",
    version=settings.api_version,
    debug=settings.debug
)

# CORS middleware
origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"/{settings.api_version}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"/{settings.api_version}/users", tags=["Users"])
app.include_router(body.router, prefix=f"/{settings.api_version}/body", tags=["Body Analysis"])
app.include_router(recommendations.router, prefix=f"/{settings.api_version}/recommendations", tags=["Recommendations"])
app.include_router(products.router, prefix=f"/{settings.api_version}/products", tags=["Products"])
app.include_router(brands.router, prefix=f"/{settings.api_version}/brands", tags=["Brands"])
app.include_router(analytics.router, prefix=f"/{settings.api_version}/analytics", tags=["Analytics"])

if settings.enable_admin_api:
    app.include_router(admin.router, prefix=f"/{settings.api_version}/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.api_version,
        "status": "running",
        "environment": settings.app_env
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc) if settings.debug else None}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
