import os
import json
import logging
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session
from pypdf import PdfReader
import docx

from app.core.deps import get_current_active_user, get_db
from app.db.models import Resume
from app.schemas.resume import ResumeUploadResponse, ResumeAnalysisResponse, SemanticSearchResponse, SemanticSearchResult, ResumeHistoryItem
from app.services.ai_service import ResumeAnalysisService
from app.services.vector_store import vector_store_service

router = APIRouter()
storage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../storage")
os.makedirs(storage_dir, exist_ok=True)

@router.post("/upload", response_model=ResumeUploadResponse)
def upload_resume(
    file: UploadFile = File(...), 
    job_description: str = Form(...),
    current_user=Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF and DOCX resumes are supported")

    filename = f"resume_{current_user.id}_{file.filename}"
    file_path = os.path.join(storage_dir, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        extracted_text = ""
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file_path)
            extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file_path)
            extracted_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            
        if len(extracted_text.strip()) < 50:
            raise ValueError("Extracted text is too short. Resume might be an image-based PDF or empty.")
            
        logging.info(f"Extracted {len(extracted_text)} characters from {file.filename}")
        logging.info(f"Job description length: {len(job_description)} characters")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to extract text from resume: {str(e)}")

    try:
        analysis = ResumeAnalysisService.analyze_resume(extracted_text, job_description)
        
        resume = Resume(
            user_id=current_user.id,
            file_url=file_path,
            job_description=job_description,
            ats_score=analysis["ats_score"],
            skills_match=analysis["skills_match"],
            experience_match=analysis["experience_match"],
            keyword_match=analysis["keyword_match"],
            education_match=analysis["education_match"],
            formatting_score=analysis["formatting_score"],
            strengths=json.dumps(analysis["strengths"]),
            weaknesses=json.dumps(analysis["weaknesses"]),
            missing_skills=json.dumps(analysis["missing_skills"]),
            improvement_suggestions=json.dumps(analysis["recommendations"]),
            extracted_text=extracted_text,
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)

        # Add to vector store for semantic search
        vector_store_service.add_resume(
            resume_id=resume.id,
            user_id=current_user.id,
            text=extracted_text,
            metadata={"filename": file.filename}
        )

        return ResumeUploadResponse(
            ats_score=analysis["ats_score"],
            skills_match=analysis["skills_match"],
            experience_match=analysis["experience_match"],
            keyword_match=analysis["keyword_match"],
            education_match=analysis["education_match"],
            formatting_score=analysis["formatting_score"],
            matched_skills=analysis.get("matched_skills", []),
            missing_skills=analysis.get("missing_skills", []),
            strengths=analysis.get("strengths", []),
            weaknesses=analysis.get("weaknesses", []),
            recommendations=analysis.get("recommendations", []),
            recommended_roles=analysis.get("recommended_roles", []),
        )
    except Exception as e:
        logging.error(f"Resume analysis failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Resume analysis failed: {str(e)}")


@router.get("/analysis", response_model=ResumeAnalysisResponse)
def get_resume_analysis(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.id.desc())
        .first()
    )
    
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")
    
    # Calculate placement readiness using Gemini
    readiness_score, feedback = ResumeAnalysisService.calculate_placement_readiness(
        resume.extracted_text or "",
        user_profile=current_user.name
    )

    try:
        matched_skills = json.loads(resume.missing_skills or "[]") if not hasattr(resume, 'matched_skills') else [] # Fallback
        missing_skills = json.loads(resume.missing_skills or "[]")
        strengths = json.loads(resume.strengths or "[]")
        weaknesses = json.loads(resume.weaknesses or "[]")
        recommendations = json.loads(resume.improvement_suggestions or "[]")
    except:
        matched_skills = []
        missing_skills = []
        strengths = []
        weaknesses = []
        recommendations = []

    return ResumeAnalysisResponse(
        ats_score=resume.ats_score or 0,
        skills_match=resume.skills_match or 0,
        experience_match=resume.experience_match or 0,
        keyword_match=resume.keyword_match or 0,
        education_match=resume.education_match or 0,
        formatting_score=resume.formatting_score or 0,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
        recommended_roles=[],
        extracted_text=resume.extracted_text,
        placement_readiness=readiness_score,
        feedback=feedback
    )

@router.get("/history", response_model=list[ResumeHistoryItem])
def get_resume_history(current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.id.desc()).all()
    
    return [
        ResumeHistoryItem(
            id=r.id,
            uploaded_at=r.uploaded_at.isoformat(),
            ats_score=r.ats_score or 0,
            skills_match=r.skills_match or 0,
            experience_match=r.experience_match or 0,
            keyword_match=r.keyword_match or 0,
            education_match=r.education_match or 0,
            formatting_score=r.formatting_score or 0,
        ) for r in resumes
    ]

@router.get("/search", response_model=SemanticSearchResponse)
def search_resumes(query: str = Query(..., description="Semantic search query"), current_user=Depends(get_current_active_user)):
    """Search for resumes matching a query semantically"""
    try:
        results = vector_store_service.semantic_search(query=query, user_id=current_user.id, limit=5)
        formatted = [
            SemanticSearchResult(
                resume_id=r["resume_id"],
                user_id=r["user_id"],
                content_preview=r["content_preview"],
                similarity_score=r["similarity_score"]
            )
            for r in results
        ]
        return SemanticSearchResponse(results=formatted)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Semantic search failed: {str(e)}")
