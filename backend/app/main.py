from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume_routes import router as resume_router
from app.utils.config import settings


app = FastAPI(
    title="ATS Resume Analyzer API",
    description="AI-powered resume analysis API for ATS scoring and skill matching.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api/v1", tags=["Resume Analysis"])


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ATS Resume Analyzer API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
