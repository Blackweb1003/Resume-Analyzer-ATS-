from app.schemas.analysis_schema import AnalysisResponse
from app.services.scoring_service import calculate_ats_score, get_detected_resume_skills
from app.services.skill_service import compare_skills
from app.services.suggestion_service import generate_suggestions


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResponse:
    ats_score = calculate_ats_score(resume_text, job_description)
    matched_skills, missing_skills = compare_skills(resume_text, job_description)
    detected_resume_skills = get_detected_resume_skills(resume_text)
    suggestions = generate_suggestions(
        ats_score=ats_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )

    return AnalysisResponse(
        ats_score=ats_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        detected_resume_skills=detected_resume_skills,
        suggestions=suggestions,
    )
