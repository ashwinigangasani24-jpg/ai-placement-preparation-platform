"""
Groq AI Service using LangChain for Resume Analysis, Interview Generation, and Career Recommendations
"""

import json
import logging
from typing import Dict, List, Tuple, Optional
from app.core.config import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
import re

def get_llm(temperature=0.7):
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    return ChatGroq(
        model_name=settings.GROQ_MODEL,
        groq_api_key=settings.GROQ_API_KEY,
        temperature=temperature,
    )

def extract_json_from_text(text: str) -> dict:
    """Helper to extract JSON object from LLM response safely"""
    try:
        # First try parsing the whole thing
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # Try finding a JSON block
            json_match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1).strip())
            
            # Try finding curly braces
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                return json.loads(text[json_start:json_end])
        except Exception:
            pass
    raise ValueError("Could not parse JSON from LLM response")

class ResumeAnalysisService:
    @staticmethod
    def _fallback_analysis(reason: str = "") -> Dict:
        if reason:
            logging.warning("Using fallback resume analysis: %s", reason)

        return {
            "ats_score": 50,
            "skills_match": 50,
            "experience_match": 50,
            "keyword_match": 50,
            "education_match": 50,
            "formatting_score": 50,
            "matched_skills": ["General matching skills"],
            "missing_skills": ["Review the job description for specific technical requirements"],
            "strengths": ["Resume content was extracted successfully"],
            "weaknesses": ["Detailed AI analysis is currently unavailable"],
            "recommendations": [
                "Ensure resume formatting is clean",
                "Add clear project sections",
                "Include skills and keywords from the job description",
            ],
            "recommended_roles": ["Intern"]
        }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def analyze_resume(resume_text: str, job_description: str) -> Dict:
        if not resume_text or len(resume_text.strip()) < 50:
            return {
                "ats_score": 0,
                "skills_match": 0,
                "experience_match": 0,
                "keyword_match": 0,
                "education_match": 0,
                "formatting_score": 0,
                "matched_skills": [],
                "missing_skills": ["Add more content to your resume"],
                "strengths": [],
                "weaknesses": ["Resume is too short"],
                "recommendations": ["Resume appears to be empty or too short"],
                "recommended_roles": ["Internship Positions"]
            }

        if not settings.GROQ_API_KEY:
            return ResumeAnalysisService._fallback_analysis("GROQ_API_KEY is not configured")
        
        prompt = PromptTemplate.from_template(
            "Analyze this resume against the provided Job Description.\n\n"
            "Resume Content:\n{resume_text}\n\n"
            "Job Description:\n{job_description}\n\n"
            "Provide a detailed analysis. You MUST return ONLY valid JSON and no other text. Follow this exact structure:\n"
            "{{\n"
            '    "skills_match_score": <number 0-40, evaluate skills matching>,\n'
            '    "experience_match_score": <number 0-25, evaluate experience/projects relevance>,\n'
            '    "keyword_match_score": <number 0-20, evaluate presence of JD keywords>,\n'
            '    "education_match_score": <number 0-10, evaluate degree/major match>,\n'
            '    "formatting_score": <number 0-5, evaluate clear structure, no clutter>,\n'
            '    "matched_skills": [<list of matching skills>],\n'
            '    "missing_critical_skills": [<list of skills required by JD but missing>],\n'
            '    "strengths": [<list of candidate strengths>],\n'
            '    "weaknesses": [<list of candidate weaknesses against JD>],\n'
            '    "resume_improvements": [<3-5 specific actionable recommendations>],\n'
            '    "suitable_roles": [<3-5 suitable internship/entry-level roles>]\n'
            "}}\n"
        )
        
        try:
            llm = get_llm(temperature=0.1)
            chain = prompt | llm
            response = chain.invoke({"resume_text": resume_text[:4000], "job_description": job_description[:4000]})
            content = response.content
            analysis = extract_json_from_text(content)
            
            # Deterministic calculation
            skills_m = int(analysis.get("skills_match_score", 20))
            exp_m = int(analysis.get("experience_match_score", 10))
            kw_m = int(analysis.get("keyword_match_score", 10))
            edu_m = int(analysis.get("education_match_score", 5))
            fmt_m = int(analysis.get("formatting_score", 3))
            
            # Cap the max scores
            skills_m = min(40, max(0, skills_m))
            exp_m = min(25, max(0, exp_m))
            kw_m = min(20, max(0, kw_m))
            edu_m = min(10, max(0, edu_m))
            fmt_m = min(5, max(0, fmt_m))
            
            ats_score = skills_m + exp_m + kw_m + edu_m + fmt_m
            
            return {
                "ats_score": ats_score,
                "skills_match": int((skills_m / 40) * 100),
                "experience_match": int((exp_m / 25) * 100),
                "keyword_match": int((kw_m / 20) * 100),
                "education_match": int((edu_m / 10) * 100),
                "formatting_score": int((fmt_m / 5) * 100),
                "matched_skills": analysis.get("matched_skills", []),
                "missing_skills": analysis.get("missing_critical_skills", []),
                "strengths": analysis.get("strengths", []),
                "weaknesses": analysis.get("weaknesses", []),
                "recommendations": analysis.get("resume_improvements", []),
                "recommended_roles": analysis.get("suitable_roles", [])
            }
        except Exception as e:
            return ResumeAnalysisService._fallback_analysis(str(e))

    @staticmethod
    def calculate_placement_readiness(resume_text: str, user_profile: str = "") -> Tuple[int, str]:
        if not settings.GROQ_API_KEY:
            return (65, "AI placement readiness is currently unavailable because GROQ_API_KEY is not configured.")

        llm = get_llm(temperature=0.5)
        prompt = PromptTemplate.from_template(
            "Based on this resume, assess the candidate's readiness for internship placement:\n\n"
            "Resume:\n{resume}\n\n"
            "Additional Profile: {profile}\n\n"
            "Provide:\n"
            "1. A readiness score (0-100)\n"
            "2. Key strengths\n"
            "3. Areas to improve\n"
            "4. Action items for next 30 days\n\n"
            "Format exactly as:\n"
            "SCORE: <number>\n"
            "FEEDBACK: <detailed assessment>"
        )
        chain = prompt | llm
        response = chain.invoke({"resume": resume_text[:3000], "profile": user_profile or 'Not provided'})
        content = response.content
        try:
            score_line = [line for line in content.split('\n') if 'SCORE:' in line][0]
            score = int(''.join(filter(str.isdigit, score_line.split(':')[1])))
            feedback_line = [line for line in content.split('\n') if 'FEEDBACK:' in line]
            feedback = feedback_line[0].replace('FEEDBACK:', '').strip() if feedback_line else content[:500]
            return (min(100, max(0, score)), feedback)
        except:
            return (65, content[:500] if content else "Resume shows moderate placement readiness")


class InterviewService:
    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_questions(profile: str, topic: str, domain: str, difficulty: str, num_questions: int) -> Dict[str, List[str]]:
        if not settings.GROQ_API_KEY:
            return {
                "questions": [
                    f"What is your experience with {topic}?",
                    f"Describe a challenging project you worked on in {domain}.",
                    f"How do you handle difficult situations when working with {topic}?",
                    f"Explain a core concept of {domain} to a non-technical person."
                ][:num_questions]
            }

        llm = get_llm(temperature=0.7)
        prompt = PromptTemplate.from_template(
            "Generate {num_questions} realistic and unique interview questions for:\n"
            "Profile: {profile}\n"
            "Role/Topic: {topic}\n"
            "Domain: {domain}\n"
            "Difficulty Level: {difficulty}\n\n"
            "Provide a mix of technical, scenario-based, and behavioral questions. Ensure they do not repeat.\n"
            "You MUST return ONLY valid JSON and no other text. Return the questions as a JSON array of strings under the key 'questions':\n"
            "{{\n"
            '    "questions": ["Q1", "Q2", "Q3", ...]\n'
            "}}\n"
        )
        chain = prompt | llm
        response = chain.invoke({
            "profile": profile, 
            "topic": topic, 
            "domain": domain, 
            "difficulty": difficulty,
            "num_questions": num_questions
        })
        content = response.content
        try:
            questions = extract_json_from_text(content)
            return {
                "questions": questions.get("questions", [])
            }
        except Exception:
            return {
                "questions": [f"Explain a key concept in {domain} related to {topic}."] * num_questions
            }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def evaluate_interview(questions: List[str], answers: List[str], domain: str) -> Dict:
        if not settings.GROQ_API_KEY:
            return {
                "overall_score": 75,
                "technical_score": 70,
                "communication_score": 80,
                "confidence_score": 75,
                "strengths": ["Clear communication", "Basic understanding of concepts"],
                "areas_to_improve": ["Provide more detailed examples", "Deepen technical knowledge"],
                "learning_resources": ["Review official documentation", "Practice more mock interviews"],
                "domain_performance": f"Demonstrated foundational knowledge in {domain}. Further practice recommended."
            }

        llm = get_llm(temperature=0.2)
        
        transcript = ""
        for i, (q, a) in enumerate(zip(questions, answers)):
            transcript += f"Q{i+1}: {q}\nAnswer: {a}\n\n"
            
        prompt = PromptTemplate.from_template(
            "Evaluate this entire mock interview transcript for the {domain} domain.\n\n"
            "Transcript:\n{transcript}\n\n"
            "You MUST return ONLY valid JSON and no other text. Provide a detailed evaluation as JSON with the exact keys:\n"
            "{{\n"
            '    "overall_score": <0-100>,\n'
            '    "technical_score": <0-100>,\n'
            '    "communication_score": <0-100>,\n'
            '    "confidence_score": <0-100>,\n'
            '    "strengths": ["Strength 1", "Strength 2"],\n'
            '    "areas_to_improve": ["Area 1", "Area 2"],\n'
            '    "learning_resources": ["Resource 1", "Resource 2"],\n'
            '    "domain_performance": "Brief paragraph summarizing their performance in {domain}"\n'
            "}}\n"
        )
        chain = prompt | llm
        response = chain.invoke({"domain": domain, "transcript": transcript})
        content = response.content
        try:
            evaluation = extract_json_from_text(content)
            return evaluation
        except Exception:
            return {
                "overall_score": 70,
                "technical_score": 70,
                "communication_score": 70,
                "confidence_score": 70,
                "strengths": ["Completed the interview"],
                "areas_to_improve": ["Provide more detailed answers"],
                "learning_resources": ["Review domain fundamentals"],
                "domain_performance": "Average performance."
            }


class CareerService:
    @staticmethod
    def generate_recommendations(profile: str, skills: List[str], interests: str = "") -> Dict[str, any]:
        if not settings.GROQ_API_KEY:
            return {
                "roadmap": ["Master fundamentals in your field", "Build a portfolio project", "Prepare for interviews", "Apply for internships"],
                "certifications": ["Relevant fundamental certification"],
                "career_path": "Junior/Intern -> Mid-level -> Senior",
                "next_steps": ["Update resume", "Practice technical skills", "Network with professionals"]
            }

        llm = get_llm(temperature=0.6)
        prompt = PromptTemplate.from_template(
            "Generate a personalized career development plan for:\n\n"
            "Profile: {profile}\n"
            "Current Skills: {skills}\n"
            "Interests: {interests}\n\n"
            "You MUST return ONLY valid JSON and no other text. Provide as JSON:\n"
            "{{\n"
            '    "learning_roadmap": [<5-7 specific learning milestones/steps>],\n'
            '    "recommended_certifications": [<3-4 relevant certifications>],\n'
            '    "career_trajectory": "<2-3 sentences about potential career path>",\n'
            '    "next_30_days": [<3 specific actions for next month>]\n'
            "}}\n"
        )
        chain = prompt | llm
        response = chain.invoke({
            "profile": profile,
            "skills": ', '.join(skills) if skills else 'Not specified',
            "interests": interests or 'General tech career'
        })
        content = response.content
        try:
            recommendations = extract_json_from_text(content)
            return {
                "roadmap": recommendations.get("learning_roadmap", []),
                "certifications": recommendations.get("recommended_certifications", []),
                "career_path": recommendations.get("career_trajectory", ""),
                "next_steps": recommendations.get("next_30_days", [])
            }
        except Exception:
            return {
                "roadmap": ["Master fundamentals"],
                "certifications": ["Relevant Certs"],
                "career_path": "Junior -> Mid-level.",
                "next_steps": ["Build a project"]
            }

    @staticmethod
    def suggest_skills_to_learn(current_skills: List[str], target_role: str) -> Dict[str, List[str]]:
        if not settings.GROQ_API_KEY:
            return {
                "immediate_skills": ["Core programming languages", "Version control", "Basic frameworks"],
                "advanced_skills": ["System design", "Cloud platforms", "Advanced optimization"],
                "resources": "Online learning platforms (Coursera, Udemy, edX)"
            }

        llm = get_llm(temperature=0.6)
        prompt = PromptTemplate.from_template(
            "Analyze skill gaps for {target_role} role:\n\n"
            "Current Skills: {skills}\n\n"
            "You MUST return ONLY valid JSON and no other text. Provide essential and advanced skills needed as JSON:\n"
            "{{\n"
            '    "immediate_skills": [<5-6 skills to learn immediately>],\n'
            '    "advanced_skills": [<4-5 skills for career growth>],\n'
            '    "learning_resources": "<recommendation for where to learn>"\n'
            "}}\n"
        )
        chain = prompt | llm
        response = chain.invoke({
            "target_role": target_role,
            "skills": ', '.join(current_skills) if current_skills else 'Entry-level'
        })
        content = response.content
        try:
            skills_data = extract_json_from_text(content)
            return {
                "immediate_skills": skills_data.get("immediate_skills", []),
                "advanced_skills": skills_data.get("advanced_skills", []),
                "resources": skills_data.get("learning_resources", "")
            }
        except Exception:
            return {
                "immediate_skills": ["SQL", "Web Dev"],
                "advanced_skills": ["Cloud Platforms"],
                "resources": "Online platforms"
            }
