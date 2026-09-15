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
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text

    output_items = getattr(response, "output", None) or []
    text_parts: list[str] = []

    for item in output_items:
        content_items = getattr(item, "content", None)
        if isinstance(item, dict):
            content_items = item.get("content")

        for content in content_items or []:
            text = getattr(content, "text", None)
            if isinstance(content, dict):
                text = content.get("text")
            if text:
                text_parts.append(text)

    return "\n".join(text_parts).strip()


def analyze_resume_context(
    *,
    resume_text: str,
    job_description: str,
) -> tuple[LLMAnalysisResponse | None, str | None]:
    if not settings.openai_api_key:
        return None, GENERIC_LLM_ERROR

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
        )
        response = client.responses.create(
            model=settings.openai_model,
            instructions=SYSTEM_PROMPT,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": _build_user_prompt(resume_text, job_description),
                        }
                    ],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "resume_contextual_analysis",
                    "strict": True,
                    "schema": LLMAnalysisResponse.model_json_schema(),
                }
            },
            max_output_tokens=2500,
            truncation="auto",
        )

        if getattr(response, "status", "completed") != "completed":
            return None, GENERIC_LLM_ERROR

        output_text = _extract_output_text(response)
        if not output_text:
            return None, GENERIC_LLM_ERROR

        return LLMAnalysisResponse.model_validate_json(output_text), None
    except (ImportError, ValidationError, ValueError, TypeError):
        return None, GENERIC_LLM_ERROR
    except Exception:
        return None, GENERIC_LLM_ERROR
