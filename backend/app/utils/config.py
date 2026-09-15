import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:
    cors_origins: list[str]
    embedding_model_name: str
    openai_api_key: str | None
    openai_model: str
    openai_timeout_seconds: float
    llm_max_resume_chars: int
    llm_max_job_description_chars: int

    def __init__(self) -> None:
        raw_origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
        self.cors_origins = [
            origin.strip()
            for origin in raw_origins.split(",")
            if origin.strip()
        ]
        self.embedding_model_name = os.getenv(
            "EMBEDDING_MODEL_NAME",
            "all-MiniLM-L6-v2",
        )
        self.openai_api_key = os.getenv("OPENAI_API_KEY") or None
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.openai_timeout_seconds = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "30"))
        self.llm_max_resume_chars = int(os.getenv("LLM_MAX_RESUME_CHARS", "20000"))
        self.llm_max_job_description_chars = int(
            os.getenv("LLM_MAX_JOB_DESCRIPTION_CHARS", "12000")
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
