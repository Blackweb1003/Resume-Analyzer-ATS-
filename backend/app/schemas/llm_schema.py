from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SkillEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill: str = Field(..., min_length=1)
    evidence: str = Field(..., min_length=1)
    evidence_strength: Literal["explicit", "weak", "none"]


class LLMAnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_skills: list[str] = Field(..., max_length=30)
    preferred_skills: list[str] = Field(..., max_length=30)
    matched_skills: list[str] = Field(..., max_length=30)
    missing_skills: list[str] = Field(..., max_length=30)
    skill_evidence: list[SkillEvidence] = Field(..., max_length=30)
    experience_relevance: float = Field(..., ge=0.0, le=1.0)
    project_relevance: float = Field(..., ge=0.0, le=1.0)
    contextual_skill_alignment: float = Field(..., ge=0.0, le=1.0)
    strengths: list[str] = Field(..., max_length=8)
    weaknesses: list[str] = Field(..., max_length=8)
    suggestions: list[str] = Field(..., max_length=8)
    explanation: str = Field(..., min_length=1, max_length=1200)
