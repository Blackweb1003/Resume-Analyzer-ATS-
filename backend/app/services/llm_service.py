from pydantic import ValidationError

from app.schemas.llm_schema import LLMAnalysisResponse
from app.utils.config import settings


GENERIC_LLM_ERROR = "Contextual analysis temporarily unavailable"


SYSTEM_PROMPT = """
You analyze a candidate resume against a job description for an ATS-style resume
assistant. Use only evidence contained in the supplied resume and job
description. Do not invent skills, employment, projects, certifications,
education, or experience.

Rules:
- Separate required skills from preferred or nice-to-have skills.
- A keyword appearing once does not automatically prove proficiency.
- Distinguish explicit evidence, weak evidence, and no evidence.
- Understand synonyms and related terminology, but do not claim a skill is
  present without reasonable resume evidence.
- Evaluate experience and project relevance to the job description.
- Keep suggestions truthful, actionable, and grounded in the supplied text.
- Never recommend lying or adding experience the candidate does not have.
- Return only data that fits the requested JSON schema.
"""


def _trim_text(text: str, max_chars: int) -> str:
    stripped = text.strip()
    if len(stripped) <= max_chars:
        return stripped

    return stripped[:max_chars]


def _build_user_prompt(resume_text: str, job_description: str) -> str:
    trimmed_resume = _trim_text(resume_text, settings.llm_max_resume_chars)
    trimmed_job_description = _trim_text(
        job_description,
        settings.llm_max_job_description_chars,
    )

    return f"""
Analyze this resume against this job description.

Score dimensions must be normalized from 0.0 to 1.0:
- experience_relevance: relevance of candidate experience to the JD
- project_relevance: relevance of candidate projects to the JD
- contextual_skill_alignment: skill alignment including synonyms and related terms

For skill_evidence, include important required/preferred skills and mark each as:
- explicit: strong resume evidence
- weak: partial, indirect, or shallow evidence
- none: no reasonable resume evidence

RESUME:
{trimmed_resume}

JOB DESCRIPTION:
{trimmed_job_description}
"""


def _extract_output_text(response: object) -> str:
    return (getattr(response, "text", None) or "").strip()


def analyze_resume_context(
    *,
    resume_text: str,
    job_description: str,
) -> tuple[LLMAnalysisResponse | None, str | None]:
    if not settings.google_api_key:
        return None, GENERIC_LLM_ERROR

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=settings.google_api_key,
            http_options=types.HttpOptions(
                timeout=int(settings.llm_timeout_seconds * 1000),
            ),
        )
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=_build_user_prompt(resume_text, job_description),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=LLMAnalysisResponse,
                max_output_tokens=2500,
            ),
        )

        output_text = _extract_output_text(response)
        if not output_text:
            return None, GENERIC_LLM_ERROR

        return LLMAnalysisResponse.model_validate_json(output_text), None
    except (ImportError, ValidationError, ValueError, TypeError):
        return None, GENERIC_LLM_ERROR
    except Exception:
        return None, GENERIC_LLM_ERROR
