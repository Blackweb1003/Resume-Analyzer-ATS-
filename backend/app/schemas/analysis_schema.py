from pydantic import BaseModel, Field

from app.schemas.llm_schema import SkillEvidence


class AnalysisResponse(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)
    base_score: int = Field(..., ge=0, le=100)
    skill_score: int = Field(..., ge=0, le=100)
    keyword_score: int = Field(..., ge=0, le=100)
    semantic_score: int = Field(..., ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    detected_resume_skills: list[str]
    suggestions: list[str]
    llm_analysis_available: bool = False
    llm_error: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    contextual_matched_skills: list[str] = Field(default_factory=list)
    contextual_missing_skills: list[str] = Field(default_factory=list)
    skill_evidence: list[SkillEvidence] = Field(default_factory=list)
    experience_relevance: int | None = Field(default=None, ge=0, le=100)
    project_relevance: int | None = Field(default=None, ge=0, le=100)
    contextual_skill_alignment: int | None = Field(default=None, ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    llm_explanation: str | None = None
