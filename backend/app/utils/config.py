import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:
    cors_origins: list[str]
    embedding_model_name: str

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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
