from app.schemas.analysis_schema import AnalysisResponse
from app.schemas.llm_schema import LLMAnalysisResponse
from app.services.llm_service import analyze_resume_context
from app.services.scoring_service import (
    calculate_hybrid_ats_score,
    calculate_llm_context_score,
    calculate_objective_score_breakdown,
    get_detected_resume_skills,
    score_to_percent,
)
from app.services.skill_service import compare_skills
from app.services.suggestion_service import generate_suggestions


def _merge_suggestions(
    rule_based_suggestions: list[str],
    llm_analysis: LLMAnalysisResponse | None,
) -> list[str]:
    llm_suggestions = llm_analysis.suggestions if llm_analysis else []
    merged: list[str] = []
    seen: set[str] = set()

    for suggestion in [*llm_suggestions, *rule_based_suggestions]:
        cleaned = suggestion.strip()
        key = cleaned.lower()
        if cleaned and key not in seen:
            merged.append(cleaned)
            seen.add(key)

    return merged


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResponse:
    objective_breakdown = calculate_objective_score_breakdown(
        resume_text,
        job_description,
    )
    matched_skills, missing_skills = compare_skills(resume_text, job_description)
    detected_resume_skills = get_detected_resume_skills(resume_text)
    rule_based_suggestions = generate_suggestions(
        ats_score=objective_breakdown.base_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )
    llm_analysis, llm_error = analyze_resume_context(
        resume_text=resume_text,
        job_description=job_description,
    )

    llm_context_score = None
    if llm_analysis:
        llm_context_score = calculate_llm_context_score(
            experience_relevance=llm_analysis.experience_relevance,
            project_relevance=llm_analysis.project_relevance,
            contextual_skill_alignment=llm_analysis.contextual_skill_alignment,
        )

    ats_score = calculate_hybrid_ats_score(
        objective_score=objective_breakdown.objective_score,
        llm_context_score=llm_context_score,
    )
    suggestions = _merge_suggestions(rule_based_suggestions, llm_analysis)

    return AnalysisResponse(
        ats_score=ats_score,
        base_score=objective_breakdown.base_score,
        skill_score=objective_breakdown.skill_score_percent,
        keyword_score=objective_breakdown.keyword_score_percent,
        semantic_score=objective_breakdown.semantic_score_percent,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        detected_resume_skills=detected_resume_skills,
        suggestions=suggestions,
        llm_analysis_available=llm_analysis is not None,
        llm_error=None if llm_analysis else llm_error,
        required_skills=llm_analysis.required_skills if llm_analysis else [],
        preferred_skills=llm_analysis.preferred_skills if llm_analysis else [],
        contextual_matched_skills=llm_analysis.matched_skills if llm_analysis else [],
        contextual_missing_skills=llm_analysis.missing_skills if llm_analysis else [],
        skill_evidence=llm_analysis.skill_evidence if llm_analysis else [],
        experience_relevance=(
            score_to_percent(llm_analysis.experience_relevance)
            if llm_analysis
            else None
        ),
        project_relevance=(
            score_to_percent(llm_analysis.project_relevance)
            if llm_analysis
            else None
        ),
        contextual_skill_alignment=(
            score_to_percent(llm_analysis.contextual_skill_alignment)
            if llm_analysis
            else None
        ),
        strengths=llm_analysis.strengths if llm_analysis else [],
        weaknesses=llm_analysis.weaknesses if llm_analysis else [],
        llm_explanation=llm_analysis.explanation if llm_analysis else None,
    )
