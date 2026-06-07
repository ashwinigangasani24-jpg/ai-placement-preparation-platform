from pydantic import BaseModel
from typing import Dict


class DashboardResponse(BaseModel):
    ats_score: int
    placement_readiness: int
    interview_score: int
    internship_statistics: Dict[str, int]
    recent_activity: Dict[str, int]
