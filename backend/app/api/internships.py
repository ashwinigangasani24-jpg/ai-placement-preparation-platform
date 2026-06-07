from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_current_active_user, get_db
from app.db.models import Internship, InternshipStatus
from app.schemas.resume import ResumeAnalysisResponse
from pydantic import BaseModel

router = APIRouter()


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
        orm_mode = True


@router.post("/", response_model=InternshipResponse)
def create_internship(payload: InternshipRequest, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    internship = Internship(
        user_id=current_user.id,
        company_name=payload.company_name,
        role=payload.role,
        status=payload.status,
    )
    db.add(internship)
    db.commit()
    db.refresh(internship)
    return internship


@router.get("/", response_model=List[InternshipResponse])
def list_internships(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(Internship).filter(Internship.user_id == current_user.id).all()
