from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, resume, interview, internships, career, dashboard
from app.db import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

from app.core.config import settings
import logging

app = FastAPI(
    title="AI Internship & Placement Intelligence Platform",
    description="MVP backend for student placement readiness using AI services.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    if not settings.GROQ_API_KEY:
        logging.error("CRITICAL ERROR: GROQ_API_KEY is not set in environment variables.")
        # We don't exit to prevent crashing the whole app, but log it as critical
        logging.warning("AI features will not work without GROQ_API_KEY.")


# CORS middleware with explicit preflight handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://ai-placement-preparation-platform.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint for deployment verification."""
    return {"status": "ok", "service": "placement-intelligence-api"}


@app.get("/")
async def root():
    """Root endpoint with API documentation link."""
    return {
        "message": "AI Internship & Placement Intelligence Platform API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(internships.router, prefix="/api/internships", tags=["internships"])
app.include_router(career.router, prefix="/api/career", tags=["career"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )
