from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_active_user, get_db
from app.db.models import Resume, InterviewResult, Internship, InternshipStatus
from app.services.ai_service import ResumeAnalysisService
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()


class DashboardResponse(BaseModel):
    ats_score: int
    placement_readiness: int
    interview_score: int
    internship_statistics: Dict[str, int]
    recent_activity: Dict[str, int]
    placement_feedback: str = ""


@router.get("/", response_model=DashboardResponse)
def get_dashboard(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard with placement readiness assessment using Gemini AI
    
    Returns:
    - ATS score from latest resume
    - Gemini-powered placement readiness score
    - Latest interview score
    - Internship application statistics
    - Recent activity metrics
    """
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
        .first()
    )
    
    avg_interview_score = (
        db.query(InterviewResult)
        .filter(InterviewResult.user_id == current_user.id)
        .order_by(InterviewResult.created_at.desc())
        .first()
    )
    
    internships = db.query(Internship).filter(Internship.user_id == current_user.id).all()
    status_counts = {status.value: 0 for status in InternshipStatus}
    for internship in internships:
        status_counts[internship.status.value] = status_counts.get(internship.status.value, 0) + 1

    # Calculate placement readiness using Gemini AI
    placement_readiness = 30  # default
    placement_feedback = "No resume uploaded yet. Upload your resume to get personalized placement readiness assessment."
    
    if latest_resume and latest_resume.extracted_text:
        try:
            placement_readiness, placement_feedback = ResumeAnalysisService.calculate_placement_readiness(
                latest_resume.extracted_text,
                user_profile=current_user.name or "Student"
            )
        except Exception as e:
            # Fallback calculation if Gemini fails
            placement_readiness = min(100, latest_resume.ats_score + 20) if latest_resume.ats_score else 50
            placement_feedback = f"Resume-based assessment: {placement_readiness}/100"

    return DashboardResponse(
        ats_score=latest_resume.ats_score or 0 if latest_resume else 0,
        placement_readiness=placement_readiness,
        interview_score=avg_interview_score.score if avg_interview_score else 0,
        internship_statistics=status_counts,
        recent_activity={
            "internships": len(internships),
            "interviews": db.query(InterviewResult).filter(InterviewResult.user_id == current_user.id).count(),
        },
        placement_feedback=placement_feedback,
    )
