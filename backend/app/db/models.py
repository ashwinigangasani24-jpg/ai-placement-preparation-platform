from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
    interviews = relationship("InterviewResult", back_populates="user")
    internships = relationship("Internship", back_populates="user")
    career_recommendations = relationship("CareerRecommendation", back_populates="user")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_url = Column(String(512), nullable=False)
    job_description = Column(Text, nullable=True)
    ats_score = Column(Integer, nullable=True)
    skills_match = Column(Integer, nullable=True)
    experience_match = Column(Integer, nullable=True)
    keyword_match = Column(Integer, nullable=True)
    education_match = Column(Integer, nullable=True)
    formatting_score = Column(Integer, nullable=True)
    strengths = Column(Text, nullable=True) # JSON string array
    weaknesses = Column(Text, nullable=True) # JSON string array
    missing_skills = Column(Text, nullable=True) # JSON string array
    improvement_suggestions = Column(Text, nullable=True) # JSON string array
    extracted_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class InterviewResult(Base):
    __tablename__ = "interview_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)
    domain = Column(String(128), nullable=True)
    status = Column(String(64), default="Completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interviews")


class InternshipStatus(str, enum.Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offered = "Offered"
    rejected = "Rejected"
    accepted = "Accepted"


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(256), nullable=False)
    role = Column(String(256), nullable=False)
    status = Column(Enum(InternshipStatus), default=InternshipStatus.applied, nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="internships")


class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    roadmap = Column(Text, nullable=False)
    certifications = Column(Text, nullable=False)
    career_path = Column(Text, nullable=False)

    user = relationship("User", back_populates="career_recommendations")
