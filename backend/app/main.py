import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from app.api import auth, resume, interview, internships, career, dashboard
    from app.db import models
    from app.db.session import engine

    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        import logging
        logging.warning(f"Skipping database creation during startup: {e}")

    from app.core.config import settings
    import logging
except Exception as e:
    import traceback
    print("CRASHED ON IMPORT: ", e)
    traceback.print_exc()
    raise

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
origins = list(dict.fromkeys(settings.CORS_ORIGINS + [
    "https://ai-placement-preparation-platform.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000"
]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint for deployment verification."""
    return {"status": "ok", "service": "placement-intelligence-api"}


@app.get("/api/diagnose")
async def diagnose_groq():
    """Diagnostic endpoint to safely test Groq API configuration."""
    from app.core.config import settings
    
    key = settings.GROQ_API_KEY
    if not key:
        return {"status": "error", "message": "GROQ_API_KEY is not found in the environment variables."}
        
    diagnostic_info = {
        "key_found": True,
        "starts_with_gsk": key.startswith("gsk_"),
        "has_quotes": key.startswith('"') or key.endswith('"'),
        "has_spaces": " " in key,
        "key_length": len(key)
    }
    
    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model_name=settings.GROQ_MODEL, groq_api_key=key, temperature=0.1)
        res = llm.invoke("Say hello")
        diagnostic_info["api_test"] = "Success! Groq replied: " + str(res.content)
        diagnostic_info["status"] = "ok"
    except Exception as e:
        diagnostic_info["api_test"] = "Failed"
        diagnostic_info["error"] = str(e)
        diagnostic_info["status"] = "error"
        
    return diagnostic_info

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
