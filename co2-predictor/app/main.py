"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .core.config import settings
from .db.database import Database

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_db_client():
    """
    Connect to MongoDB on startup.
    """
    await Database.connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Close MongoDB connection on shutdown.
    """
    await Database.close_db()

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to CO2 Predictor API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs"
    } 