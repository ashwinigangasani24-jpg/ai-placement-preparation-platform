from app.db.models import Internship, InterviewResult, Resume
from sqlalchemy.orm import Session


def compute_internship_summary(db: Session, user_id: int) -> dict:
    internships = db.query(Internship).filter(Internship.user_id == user_id).all()
    summary = {status.value: 0 for status in [i.status for i in internships]}
    for internship in internships:
        summary[internship.status.value] = summary.get(internship.status.value, 0) + 1
    return summary


def compute_placement_readiness(ats_score: int, recent_interview: int) -> int:
    return min(100, int(ats_score * 0.6 + recent_interview * 0.4))
