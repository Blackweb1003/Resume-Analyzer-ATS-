import re

from app.utils.text_cleaner import normalize_text


TECHNICAL_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node",
    "node.js",
    "express",
    "fastapi",
    "django",
    "flask",
    "html",
    "css",
    "tailwind",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "transformers",
    "llm",
    "api",
    "rest api",
    "graphql",
    "ci/cd",
    "testing",
    "unit testing",
    "agile",
    "scrum",
    "data analysis",
    "data visualization",
    "power bi",
    "tableau",
}


def extract_skills(text: str) -> list[str]:
    normalized_text = normalize_text(text)
    found_skills: set[str] = set()

    for skill in TECHNICAL_SKILLS:
        skill_pattern = re.escape(skill.lower()).replace("\\ ", r"\s+")
        pattern = rf"(?<![a-z0-9.+#]){skill_pattern}(?![a-z0-9.+#])"

        if re.search(pattern, normalized_text):
            found_skills.add(skill)

    return sorted(found_skills)


def compare_skills(resume_text: str, job_description: str) -> tuple[list[str], list[str]]:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched_skills = sorted(resume_skills.intersection(jd_skills))
    missing_skills = sorted(jd_skills.difference(resume_skills))

    return matched_skills, missing_skills
