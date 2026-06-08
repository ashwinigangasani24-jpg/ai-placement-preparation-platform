from pydantic import BaseModel
from app.db.models import InternshipStatus
from typing import List


class InternshipRequest(BaseModel):
    company_name: str
    role: str
    status: InternshipStatus


class InternshipResponse(BaseModel):
    id: int
    company_name: str
    role: str
    status: InternshipStatus
    application_date: str

    class Config:
        from_attributes = True
