import re


def normalize_text(text: str) -> str:
    lowered = text.lower()
    normalized = re.sub(r"[^a-z0-9.+#/\s-]", " ", lowered)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()
