from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    detected_resume_skills: list[str]
    suggestions: list[str]
