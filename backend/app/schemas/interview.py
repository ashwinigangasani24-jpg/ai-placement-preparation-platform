from pydantic import BaseModel
from typing import List


class InterviewGenerateRequest(BaseModel):
    profile: str
    topic: str
    domain: str = "Frontend Development"
    difficulty: str = "intermediate"
    num_questions: int = 10


class InterviewGenerateResponse(BaseModel):
    questions: List[str]


class InterviewEvaluateRequest(BaseModel):
    questions: List[str]
    answers: List[str]
    domain: str
    status: str


class InterviewEvaluateResponse(BaseModel):
    overall_score: int
    technical_score: int
    communication_score: int
    confidence_score: int
    strengths: List[str]
    areas_to_improve: List[str]
    learning_resources: List[str]
    domain_performance: str
    status: str
