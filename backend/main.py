"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.settings import PODCAST_DIR, ANSWER_DIR, ENVIRONMENT, HOST, PORT

# Import route modules
from api.routes import documents, podcasts, questions

# Create FastAPI app
app = FastAPI(
    title="AI Interactive Podcast API",
    description="Generate AI-powered podcasts from documents with interactive Q&A",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
)

# CORS middleware (allow iOS app to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify iOS app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories for serving audio
app.mount("/generated/podcasts", StaticFiles(directory=PODCAST_DIR), name="podcasts")
app.mount("/generated/answers", StaticFiles(directory=ANSWER_DIR), name="answers")

# Include API routes
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(podcasts.router, prefix="/api/podcasts", tags=["podcasts"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "AI Interactive Podcast API",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs" if ENVIRONMENT == "development" else "disabled in production"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)