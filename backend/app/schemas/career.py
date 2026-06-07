from pydantic import BaseModel
from typing import List


class CareerRecommendationResponse(BaseModel):
    roadmap: List[str]
    certifications: List[str]
    career_path: str
