from functools import lru_cache

from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.skill_service import compare_skills, extract_skills
from app.utils.config import settings
from app.utils.text_cleaner import normalize_text


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


def calculate_ats_score(resume_text: str, job_description: str) -> int:
    skill_score = calculate_skill_match_score(resume_text, job_description)
    keyword_score = calculate_keyword_similarity(resume_text, job_description)
    semantic_score = calculate_semantic_similarity(resume_text, job_description)

    weighted_score = (
        skill_score * 0.45
        + keyword_score * 0.25
        + semantic_score * 0.30
    )

    return round(max(0.0, min(1.0, weighted_score)) * 100)


def get_detected_resume_skills(resume_text: str) -> list[str]:
    return extract_skills(resume_text)
