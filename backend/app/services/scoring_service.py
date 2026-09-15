from dataclasses import dataclass
from functools import lru_cache

from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.skill_service import compare_skills, extract_skills
from app.utils.config import settings
from app.utils.text_cleaner import normalize_text


@dataclass(frozen=True)
class ObjectiveScoreBreakdown:
    skill_score: float
    keyword_score: float
    semantic_score: float
    objective_score: float

    @property
    def base_score(self) -> int:
        return score_to_percent(self.objective_score)

    @property
    def skill_score_percent(self) -> int:
        return score_to_percent(self.skill_score)

    @property
    def keyword_score_percent(self) -> int:
        return score_to_percent(self.keyword_score)

    @property
    def semantic_score_percent(self) -> int:
        return score_to_percent(self.semantic_score)


def clamp_score(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def score_to_percent(value: float) -> int:
    return round(clamp_score(value) * 100)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model_name)


def calculate_keyword_similarity(resume_text: str, job_description: str) -> float:
    texts = [normalize_text(resume_text), normalize_text(job_description)]
    vectorizer = CountVectorizer(stop_words="english", ngram_range=(1, 2))

    try:
        matrix = vectorizer.fit_transform(texts)
    except ValueError:
        return 0.0

    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def calculate_semantic_similarity(resume_text: str, job_description: str) -> float:
    model = get_embedding_model()
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return max(0.0, min(1.0, float(similarity)))


def calculate_skill_match_score(resume_text: str, job_description: str) -> float:
    matched_skills, missing_skills = compare_skills(resume_text, job_description)
    total_required_skills = len(matched_skills) + len(missing_skills)

    if total_required_skills == 0:
        return 0.0

    return len(matched_skills) / total_required_skills


def calculate_objective_score_breakdown(
    resume_text: str,
    job_description: str,
) -> ObjectiveScoreBreakdown:
    skill_score = calculate_skill_match_score(resume_text, job_description)
    keyword_score = calculate_keyword_similarity(resume_text, job_description)
    semantic_score = calculate_semantic_similarity(resume_text, job_description)

    objective_score = (
        skill_score * 0.45
        + keyword_score * 0.25
        + semantic_score * 0.30
    )

    return ObjectiveScoreBreakdown(
        skill_score=clamp_score(skill_score),
        keyword_score=clamp_score(keyword_score),
        semantic_score=clamp_score(semantic_score),
        objective_score=clamp_score(objective_score),
    )


def calculate_llm_context_score(
    *,
    experience_relevance: float,
    project_relevance: float,
    contextual_skill_alignment: float,
) -> float:
    return clamp_score(
        contextual_skill_alignment * 0.50
        + experience_relevance * 0.30
        + project_relevance * 0.20
    )


def calculate_hybrid_ats_score(
    *,
    objective_score: float,
    llm_context_score: float | None,
) -> int:
    if llm_context_score is None:
        return score_to_percent(objective_score)

    # Final hybrid formula:
    # objective_score = skill*0.45 + keyword*0.25 + semantic*0.30
    # llm_context_score = contextual_skill_alignment*0.50
    #                   + experience_relevance*0.30
    #                   + project_relevance*0.20
    # final_score = objective_score*0.70 + llm_context_score*0.30
    weighted_score = objective_score * 0.70 + clamp_score(llm_context_score) * 0.30
    return score_to_percent(weighted_score)


def calculate_ats_score(resume_text: str, job_description: str) -> int:
    breakdown = calculate_objective_score_breakdown(resume_text, job_description)
    return breakdown.base_score


def get_detected_resume_skills(resume_text: str) -> list[str]:
    return extract_skills(resume_text)
