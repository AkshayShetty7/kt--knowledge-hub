"""
FastAPI application entry point.

This module creates the FastAPI application, defines basic health
and root endpoints, and registers the application's API routers.
"""

from fastapi import FastAPI

from app.api.search import router as search_router
from app.api.sources import router as sources_router


# Create the FastAPI application.
app = FastAPI(
    title="KD Knowledge Hub API",
    version="0.1.0",
)


@app.get("/")
def home():
    """
    Return a basic message confirming that the backend is running.
    """
    return {
        "message": "KD Knowledge Hub backend is running"
    }


@app.get("/health")
def health_check():
    """
    Check the health of the backend API.

    Returns:
        A status object indicating that the API is operational.
    """
    return {"status": "ok"}


# Register API routers.
app.include_router(sources_router)
app.include_router(search_router)