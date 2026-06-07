from fastapi import APIRouter, Depends
from app.schemas.interview import (
    InterviewGenerateRequest,
    InterviewGenerateResponse,
    InterviewEvaluateRequest,
    InterviewEvaluateResponse,
)
from app.core.deps import get_current_active_user, get_db
from app.db.models import InterviewResult
from app.services.ai_service import InterviewService
from datetime import datetime

router = APIRouter()


@router.post("/generate", response_model=InterviewGenerateResponse)
def generate_interview_questions(payload: InterviewGenerateRequest, current_user=Depends(get_current_active_user)):
    """
    Generate realistic interview questions using Google Gemini AI
    """
    try:
        questions_dict = InterviewService.generate_questions(
            profile=payload.profile,
            topic=payload.topic,
            domain=payload.domain,
            difficulty=payload.difficulty,
            num_questions=payload.num_questions
        )
        return InterviewGenerateResponse(
            questions=questions_dict.get("questions", [])
        )
    except Exception as e:
        import logging
        logging.error(f"Error generating questions: {str(e)}")
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Failed to generate questions. AI service is unavailable or returned an error.")


@router.post("/evaluate", response_model=InterviewEvaluateResponse)
def evaluate_interview(payload: InterviewEvaluateRequest, current_user=Depends(get_current_active_user), db=Depends(get_db)):
    """
    Evaluate interview answers using Google Gemini AI
    """
    import json
    try:
        evaluation = InterviewService.evaluate_interview(
            questions=payload.questions,
            answers=payload.answers,
            domain=payload.domain
        )
        
        # Store result
        record = InterviewResult(
            user_id=current_user.id,
            score=evaluation.get("overall_score", 0),
            feedback=json.dumps(evaluation),
            domain=payload.domain,
            status=payload.status
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return InterviewEvaluateResponse(
            overall_score=evaluation.get("overall_score", 0),
            technical_score=evaluation.get("technical_score", 0),
            communication_score=evaluation.get("communication_score", 0),
            confidence_score=evaluation.get("confidence_score", 0),
            strengths=evaluation.get("strengths", []),
            areas_to_improve=evaluation.get("areas_to_improve", []),
            learning_resources=evaluation.get("learning_resources", []),
            domain_performance=evaluation.get("domain_performance", ""),
            status=payload.status
        )
    except Exception as e:
        fallback = {
            "overall_score": 70,
            "technical_score": 70,
            "communication_score": 70,
            "confidence_score": 70,
            "strengths": ["Completed the interview"],
            "areas_to_improve": [f"Error occurred: {str(e)}"],
            "learning_resources": ["Review fundamentals"],
            "domain_performance": "Fallback evaluation."
        }
        record = InterviewResult(
            user_id=current_user.id,
            score=70,
            feedback=json.dumps(fallback),
            domain=payload.domain,
            status=payload.status
        )
        db.add(record)
        db.commit()
        
        return InterviewEvaluateResponse(
            **fallback,
            status=payload.status
        )

@router.get("/history")
def get_interview_history(current_user=Depends(get_current_active_user), db=Depends(get_db)):
    """
    Get user's interview history
    """
    results = db.query(InterviewResult).filter(InterviewResult.user_id == current_user.id).order_by(InterviewResult.created_at.desc()).all()
    history = []
    import json
    for r in results:
        try:
            details = json.loads(r.feedback)
        except:
            details = {}
        history.append({
            "id": r.id,
            "date": r.created_at.isoformat(),
            "score": r.score,
            "domain": r.domain or "General",
            "status": r.status or "Completed",
            "details": details
        })
    return history
