# Gemini AI Integration - Quick Reference Guide

## 🚀 5-Minute Setup

### Step 1: Get API Key
```bash
# Go to: https://aistudio.google.com/app/apikey
# Click "Create API Key"
# Copy the key
```

### Step 2: Configure Backend
```bash
cd backend

# Edit .env file:
GEMINI_API_KEY=AIzaSyD...your_actual_key...

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload
```

### Step 3: Verify Integration
```bash
# Check logs for:
✅ "Uvicorn running on http://0.0.0.0:8000"
✅ "Gemini AI Service: Ready"
```

---

## 📡 API Examples

### 1. Resume Upload & Analysis (Gemini)

**Request:**
```bash
curl -X POST http://localhost:8000/api/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```

**Response (Gemini-powered):**
```json
{
  "ats_score": 78,
  "missing_skills": ["Kubernetes", "System Design", "AWS"],
  "recommendations": [
    "Add containerization and orchestration experience",
    "Include system design project examples",
    "Highlight cloud deployment experience"
  ],
  "recommended_roles": [
    "Backend Engineer Intern",
    "DevOps Engineer Intern",
    "Full-Stack Developer Intern"
  ]
}
```

---

### 2. Interview Question Generation (Gemini)

**Request:**
```bash
curl -X POST http://localhost:8000/api/interview/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "Python Backend Developer",
    "topic": "Data Structures and Algorithms"
  }'
```

**Response (Gemini-generated questions):**
```json
{
  "technical_questions": [
    "Explain binary search and implement it. What is its time complexity?",
    "Design a cache with LRU eviction policy.",
    "How would you detect a cycle in a directed graph efficiently?"
  ],
  "hr_questions": [
    "Tell us about a challenging project and how you solved it",
    "Why are you interested in this internship?"
  ]
}
```

---

### 3. Interview Answer Evaluation (Gemini)

**Request:**
```bash
curl -X POST http://localhost:8000/api/interview/evaluate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      "What is polymorphism?",
      "Explain inheritance"
    ],
    "answers": [
      "Polymorphism allows objects to take multiple forms through method overriding and overloading...",
      "Inheritance allows a class to inherit properties and methods from another class..."
    ],
    "topic": "Object-Oriented Programming"
  }'
```

**Response (Gemini evaluation):**
```json
{
  "interview_score": 82,
  "feedback": "Strong conceptual understanding of OOP principles. Good examples provided. Could add implementation examples and discuss edge cases. Overall, excellent preparation for interviews."
}
```

---

### 4. Career Recommendations (Gemini)

**Request:**
```bash
curl -X GET http://localhost:8000/api/career/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (Gemini-generated roadmap):**
```json
{
  "roadmap": [
    "Master core Python fundamentals with daily LeetCode problems for 4 weeks",
    "Build 3 full-stack projects: REST API, Web Application, Data Pipeline",
    "Contribute to 5 open-source projects for real-world experience",
    "Complete system design course and practice design interviews",
    "Prepare behavioral questions and practice mock interviews",
    "Network with 10+ senior engineers through LinkedIn and communities"
  ],
  "certifications": [
    "AWS Certified Cloud Practitioner",
    "Google Cloud Associate Cloud Engineer",
    "Certified Kubernetes Administrator"
  ],
  "career_path": "Your trajectory: Python Developer Intern → Junior Backend Engineer → Senior Backend Engineer → Staff Engineer. Focus on building strong fundamentals and contributing to impactful projects.",
  "next_steps": [
    "Enroll in 'Complete Python Course' on Udemy today",
    "Start building a URL shortener API project",
    "Join 3 Python developer communities on Discord/Slack"
  ]
}
```

---

### 5. Dashboard with Placement Readiness (Gemini)

**Request:**
```bash
curl -X GET http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (Gemini-powered assessment):**
```json
{
  "ats_score": 78,
  "placement_readiness": 72,
  "interview_score": 85,
  "internship_statistics": {
    "Applied": 5,
    "Interviewing": 2,
    "Offered": 1,
    "Rejected": 1,
    "Accepted": 0
  },
  "recent_activity": {
    "internships": 9,
    "interviews": 4
  },
  "placement_feedback": "You demonstrate strong technical fundamentals and have a good track record of applications. Focus on final interview preparation and consider reaching out to mentors for mock interviews before final rounds."
}
```

---

## 🔧 Configuration

### Basic Setup (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/placement
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=AIzaSyD...your_key...
```

### Advanced Configuration

**In `backend/app/core/config.py`:**
```python
GEMINI_MODEL = "gemini-1.5-pro"      # or "gemini-1.5-flash"
GEMINI_MAX_TOKENS = 2048             # Max response length
```

**In `backend/app/services/gemini.py`:**
```python
rate_limiter = RateLimiter(calls_per_minute=60)  # Adjust limits
```

---

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY is not configured"

**Solution:**
```bash
# 1. Check .env exists
ls backend/.env

# 2. Verify API key is set
grep GEMINI_API_KEY backend/.env

# 3. Restart backend
# CTRL+C then start again
```

### Error: "Invalid API key"

**Solution:**
```bash
# 1. Go to: https://aistudio.google.com/app/apikey
# 2. Delete old key (if exists)
# 3. Generate new key
# 4. Update .env with new key
# 5. Restart backend
```

### Error: "Rate limit exceeded"

**Solution:**
```
The system automatically handles this:
- Waits 1 second
- Retries the request
- Falls back if still limited

No action needed - just wait a moment!
```

### Error: "Empty response from Gemini"

**Solution:**
```bash
# 1. Check internet connection
ping google.com

# 2. Verify API key validity
# 3. Check Gemini service status
# 4. Try again (temporary issue)

# Fallback response will be provided
```

---

## 📊 Monitoring & Debugging

### Check API Integration
```bash
# Start backend with debug
PYTHONUNBUFFERED=1 uvicorn app.main:app --reload --log-level debug
```

### Monitor API Calls
```python
# In Python shell
from app.services.gemini import call_gemini

response = call_gemini("Test prompt")
print(response)
```

### View Logs
```bash
# Backend logs show:
# - Gemini API calls
# - Rate limiting info
# - Error messages
# - Response times
```

---

## 🎯 Common Use Cases

### Use Case 1: Get Placement Readiness
```bash
# Upload resume → Auto-analyzed with Gemini
# Dashboard shows placement readiness → Based on Gemini assessment
# Career page shows recommendations → Gemini-generated roadmap
```

### Use Case 2: Prepare for Interviews
```bash
# Enter profile and topic → Gemini generates realistic questions
# Practice answers → Gemini evaluates with detailed feedback
# View score and suggestions → Improve before actual interview
```

### Use Case 3: Career Guidance
```bash
# View career page → Get Gemini-generated roadmap
# See certifications → AI-recommended based on profile
# Get 30-day plan → Actionable steps from Gemini
```

---

## ⚡ Performance Tips

### 1. Batch Requests
```python
# Instead of 10 individual calls:
# Call once with combined data
```

### 2. Cache Results
```python
# Resume analysis cached in database
# Career recommendations stored
# Don't re-analyze unless updated
```

### 3. Use Gemini 1.5 Flash
```bash
# Faster, cheaper for simple tasks:
GEMINI_MODEL=gemini-1.5-flash
```

---

## 🔐 Security Checklist

- [ ] API key in `.env` (not committed)
- [ ] Never log API keys
- [ ] Use environment variables only
- [ ] Regenerate key after exposure
- [ ] Monitor usage in Google Console
- [ ] Set rate limits appropriate to tier

---

## 📞 Quick Support

### Documentation Files
- **Setup Guide:** `GEMINI_SETUP.md`
- **Project Overview:** `README_GEMINI.md`
- **Integration Summary:** `GEMINI_INTEGRATION_SUMMARY.md`
- **API Documentation:** `http://localhost:8000/docs`

### External Resources
- [Google Gemini API](https://ai.google.dev/docs)
- [Python SDK](https://ai.google.dev/tutorials/python_quickstart)
- [Pricing](https://ai.google.dev/pricing)
- [Models](https://ai.google.dev/models)

### Get Help
1. Check `.env` file
2. Read error message carefully
3. Review troubleshooting section
4. Check API key validity
5. Restart backend server
6. Check internet connection

---

## 📈 What's Powered by Gemini

| Feature | Status | Gemini Integration |
|---------|--------|-------------------|
| Resume Analysis | ✅ | Full AI analysis with JSON parsing |
| ATS Scoring | ✅ | Intelligent content evaluation |
| Skill Extraction | ✅ | AI-powered skill identification |
| Resume Recommendations | ✅ | Context-aware improvement suggestions |
| Interview Questions | ✅ | Dynamic, realistic question generation |
| Answer Evaluation | ✅ | Intelligent scoring and feedback |
| Career Roadmap | ✅ | Personalized learning path generation |
| Certifications | ✅ | AI-recommended based on profile |
| Placement Assessment | ✅ | Comprehensive readiness evaluation |
| Dashboard Insights | ✅ | AI-powered analytics and feedback |

---

## 🎉 You're All Set!

Your project now features **Google Gemini AI** for production-grade intelligent features.

### Next Steps:
1. ✅ Configure GEMINI_API_KEY
2. ✅ Start backend
3. ✅ Test endpoints
4. ✅ Deploy to production
5. ✅ Monitor usage

**Happy coding! 🚀**
