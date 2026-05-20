from dataclasses import dataclass


@dataclass(frozen=True)
class ResumeAnalysis:
    ats_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    detected_resume_skills: list[str]
    suggestions: list[str]
