from typing import List


def generate_text(prompt: str, max_tokens: int = 200) -> str:
    # Placeholder for a local LLM integration (Llama 3 or equivalent).
    return f"[LLM response for prompt] {prompt[:120]}"


def summarize_skill_gap(skills: List[str]) -> str:
    return "Focus on the missing skills: " + ", ".join(skills)
