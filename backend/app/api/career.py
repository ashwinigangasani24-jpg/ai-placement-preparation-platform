from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_active_user, get_db
from app.db.models import CareerRecommendation, Resume
from app.services.ai_service import CareerService
from pydantic import BaseModel
from typing import List

router = APIRouter()


class CareerRecommendationResponse(BaseModel):
    roadmap: List[str]
    certifications: List[str]
    career_path: str
    next_steps: List[str] = []


@router.get("/recommendations", response_model=CareerRecommendationResponse)
def get_career_recommendations(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get personalized career recommendations using Google Gemini AI
    
    - Analyzes current profile and skills
    - Generates learning roadmap
    - Recommends certifications
    - Provides career trajectory guidance
    """
    try:
        # Try to get existing recommendation
        recommendation = (
            db.query(CareerRecommendation)
            .filter(CareerRecommendation.user_id == current_user.id)
            .order_by(CareerRecommendation.id.desc())
            .first()
        )
        
        if recommendation:
            return CareerRecommendationResponse(
                roadmap=recommendation.roadmap.split(";") if recommendation.roadmap else [],
                certifications=recommendation.certifications.split(";") if recommendation.certifications else [],
                career_path=recommendation.career_path or "",
            )
        
        # Generate new recommendations using Gemini
        # Get latest resume to understand user skills
        latest_resume = (
            db.query(Resume)
            .filter(Resume.user_id == current_user.id)
            .order_by(Resume.id.desc())
            .first()
        )
        
        # Extract skills from resume or use default
        skills = []
        if latest_resume:
            # Parse skills from resume (simplified)
            resume_text = latest_resume.extracted_text.lower()
            common_skills = ["python", "java", "javascript", "sql", "react", "django", "fastapi", "docker", "git"]
            skills = [s for s in common_skills if s in resume_text]
        
        # Generate recommendations using Gemini
        recommendations = CareerService.generate_recommendations(
            profile=current_user.name or "Software Developer",
            skills=skills or ["Communication", "Problem-solving"],
            interests="Technology and Software Development"
        )
        
        # Store recommendations
        record = CareerRecommendation(
            user_id=current_user.id,
            roadmap=";".join(recommendations["roadmap"]),
            certifications=";".join(recommendations["certifications"]),
            career_path=recommendations["career_path"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return CareerRecommendationResponse(
            roadmap=recommendations["roadmap"],
            certifications=recommendations["certifications"],
            career_path=recommendations["career_path"],
            next_steps=recommendations.get("next_steps", []),
        )
    except HTTPException:
        raise
    except Exception as e:
        # Fallback recommendations
        fallback = {
            "roadmap": [
                "Master core programming fundamentals with daily practice",
                "Build 2-3 portfolio projects demonstrating your skills",
                "Contribute to open-source projects for real-world experience",
                "Practice system design and data structures",
                "Complete industry-recognized certifications",
            ],
            "certifications": [
                "AWS Certified Cloud Practitioner",
                "Google Cloud Associate Cloud Engineer",
                "Oracle Java Associate Programmer"
            ],
            "career_path": "Intern → Junior Professional → Mid-level Engineer",
            "next_steps": [
                "Complete one online course in your target technology",
                "Start one portfolio project",
                "Join developer communities"
            ]
        }
        
        record = CareerRecommendation(
            user_id=current_user.id,
            roadmap=";".join(fallback["roadmap"]),
            certifications=";".join(fallback["certifications"]),
            career_path=fallback["career_path"],
        )
        db.add(record)
        db.commit()
        
        return CareerRecommendationResponse(**fallback)
