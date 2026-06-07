from pydantic import BaseModel
from typing import List, Optional


class ResumeUploadResponse(BaseModel):
    ats_score: int
    skills_match: int
    experience_match: int
    keyword_match: int
    education_match: int
    formatting_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    recommended_roles: List[str]

class ResumeAnalysisResponse(BaseModel):
    ats_score: int
    skills_match: int = 0
    experience_match: int = 0
    keyword_match: int = 0
    education_match: int = 0
    formatting_score: int = 0
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: List[str] = []
    recommended_roles: List[str] = []
    extracted_text: Optional[str] = None
    placement_readiness: Optional[int] = None
    feedback: Optional[str] = None

class ResumeHistoryItem(BaseModel):
    id: int
    uploaded_at: str
    ats_score: int
    skills_match: int
    experience_match: int
    keyword_match: int
    education_match: int
    formatting_score: int


class SemanticSearchResult(BaseModel):
    resume_id: int
    user_id: int
    content_preview: str
    similarity_score: float

class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult]
