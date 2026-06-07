import re
from typing import List

COMMON_SKILLS = [
    "python", "sql", "machine learning", "data analysis", "communication", "leadership",
    "teamwork", "react", "next.js", "fastapi", "postgresql", "cloud", "docker", "git"
]


def extract_keywords(text: str) -> List[str]:
    normalized = text.lower()
    return [skill for skill in COMMON_SKILLS if skill in normalized]


def calculate_ats_score(text: str) -> int:
    score = 0
    normalized = text.lower()
    if "experience" in normalized:
        score += 20
    if "projects" in normalized:
        score += 15
    if "skills" in normalized:
        score += 15
    keywords = extract_keywords(text)
    score += min(len(keywords) * 5, 30)
    return max(0, min(score, 100))


def get_missing_skills(text: str) -> List[str]:
    existing = extract_keywords(text)
    return [skill for skill in COMMON_SKILLS if skill not in existing]


def generate_resume_insights(text: str) -> dict:
    return {
        "recommendations": [
            "Add more quantifiable achievements.",
            "Highlight relevant internship or project experience.",
            "Use a clear section structure and list skills prominently.",
        ],
        "recommended_roles": ["Software Engineering Intern", "Data Analyst Intern", "Product Analyst Intern"],
    }
