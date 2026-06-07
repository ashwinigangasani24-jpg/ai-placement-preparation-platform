# Google Gemini API Integration Guide

## Overview

This project has been enhanced with **Google Gemini AI** for advanced generative AI features including:

- ✅ **Resume Analysis** - Intelligent ATS scoring, skill extraction, and recommendations
- ✅ **Placement Readiness** - AI-powered assessment of job readiness
- ✅ **Interview Preparation** - Dynamic question generation based on profile and topic
- ✅ **Interview Evaluation** - Intelligent answer evaluation with scoring and feedback
- ✅ **Career Recommendations** - Personalized learning paths and career guidance
- ✅ **Skill Gap Analysis** - Identify skills needed for target roles

## Prerequisites

- Google Account (Gmail or Google Workspace)
- API access to Google Generative AI (Gemini)
- Python 3.10+
- Node.js 18+

## Step 1: Get Your Google Gemini API Key

### Option A: Using Google AI Studio (Fastest)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key in new project"** or **"Create API Key"**
3. Select your project (or create a new one)
4. Copy the generated API key
5. **Keep this key secure** - never commit to Git

### Option B: Using Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the **Generative Language API**:
   - Go to APIs & Services → Library
   - Search "Generative Language"
   - Click and enable it
4. Go to APIs & Services → Credentials
5. Create new "API Key" credential
6. Copy the key

### Option C: Using gcloud CLI

```bash
# Install Google Cloud SDK
# Then run:
gcloud auth application-default print-access-token
```

## Step 2: Configure Environment

### Backend Setup

1. **Update `.env` file** in the `backend/` directory:

```bash
cd backend

# Edit .env file and add:
GEMINI_API_KEY=your_actual_google_gemini_api_key_here
```

**Example .env:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/placement
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=AIzaSyD3XvK...  # Replace with your actual key
```

2. **Verify environment loaded:**
```python
# Test in Python
from app.core.config import settings
print(f"API Key configured: {bool(settings.GEMINI_API_KEY)}")
```

### Frontend Setup (Optional)

Frontend doesn't need API key - all AI calls go through backend.

## Step 3: Install Dependencies

The required package is already in `requirements.txt`:

```bash
cd backend
pip install -r requirements.txt

# Specifically installs:
# - google-generativeai==0.7.2
# - requests==2.32.3
```

## Step 4: Start the Application

### Terminal 1 - Backend (with Gemini AI)

```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✅ Uvicorn running on http://0.0.0.0:8000
📚 API documentation: http://localhost:8000/docs
🤖 Gemini AI Service: Ready
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

## Step 5: Test Gemini Integration

### Using API Documentation

1. Open http://localhost:8000/docs
2. Register/Login to get auth token
3. Test endpoints:

#### Test Resume Analysis (Gemini)
```bash
curl -X POST http://localhost:8000/api/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@path/to/resume.pdf"
```

**Response includes Gemini analysis:**
```json
{
  "ats_score": 78,
  "missing_skills": ["Docker", "Kubernetes", "AWS"],
  "recommendations": [
    "Add containerization experience",
    "Include cloud deployment examples",
    "Highlight distributed systems projects"
  ],
  "recommended_roles": [
    "Backend Engineer Intern",
    "DevOps Intern",
    "Full-stack Developer Intern"
  ]
}
```

#### Test Interview Generation (Gemini)
```bash
curl -X POST http://localhost:8000/api/interview/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "Python Developer",
    "topic": "Data Structures and Algorithms"
  }'
```

**Response with Gemini-generated questions:**
```json
{
  "technical_questions": [
    "Explain the time and space complexity of quicksort algorithm and when to use it",
    "Design a cache with LRU eviction policy and discuss your implementation",
    "How would you detect cycles in a directed graph efficiently?"
  ],
  "hr_questions": [
    "Tell us about a time you had to debug a complex production issue",
    "Why are you interested in joining our team?"
  ]
}
```

#### Test Interview Evaluation (Gemini)
```bash
curl -X POST http://localhost:8000/api/interview/evaluate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "questions": ["What is polymorphism?"],
    "answers": ["Polymorphism allows objects to take multiple forms..."],
    "topic": "OOP Concepts"
  }'
```

**Response with Gemini evaluation:**
```json
{
  "interview_score": 82,
  "feedback": "Strong conceptual understanding. Good use of examples. Could add real-world implementation details."
}
```

#### Test Career Recommendations (Gemini)
```bash
curl -X GET http://localhost:8000/api/career/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response with Gemini-generated roadmap:**
```json
{
  "roadmap": [
    "Master Python and SQL fundamentals with daily LeetCode problems",
    "Build 3 end-to-end projects (web app, data pipeline, API)",
    "Contribute to 5 open-source repositories",
    "Complete system design course and practice",
    "Prepare technical interview materials",
    "Network with senior engineers and apply to internships"
  ],
  "certifications": [
    "AWS Certified Cloud Practitioner",
    "Google Cloud Associate Cloud Engineer",
    "Certified Kubernetes Administrator (CKA)"
  ],
  "career_path": "Your career path: Python Developer Intern → Junior Backend Engineer → Senior Backend Engineer. Focus on building strong fundamentals and contributing to real products.",
  "next_steps": [
    "Complete 'The Complete Python Course' on Udemy",
    "Build a full-stack blog application with Django",
    "Join a Python developer community on Discord/Slack"
  ]
}
```

### Web Interface Testing

1. Open http://localhost:3000
2. Register account
3. Login
4. Navigate to each feature:

**Resume Page** (`/resume`)
- Upload PDF
- See Gemini analysis with ATS score
- View skill gaps and recommendations

**Interview Page** (`/interview`)
- Enter profile and topic
- Generate Gemini questions
- Answer questions
- Get Gemini evaluation with score and feedback

**Career Page** (`/career`)
- View personalized Gemini roadmap
- See recommended certifications
- Get actionable next steps

**Dashboard** (`/dashboard`)
- See overall placement readiness (Gemini score)
- View placement feedback
- Track statistics

## API Rate Limiting

The Gemini service includes built-in rate limiting:

```python
# From gemini.py
class RateLimiter:
    def __init__(self, calls_per_minute: int = 60):
        # Allows 60 API calls per minute
        # Automatically waits if limit exceeded
```

**Limits:**
- 60 calls per minute (free tier)
- Automatic exponential backoff on rate limiting
- Graceful fallbacks if API is unavailable

## Troubleshooting

### Issue: "GEMINI_API_KEY is not configured"

**Solution:**
1. Check `.env` file exists in `backend/` directory
2. Verify `GEMINI_API_KEY=` line is present
3. Ensure key is not empty
4. Restart backend server

```bash
# Debug
cd backend
python -c "from app.core.config import settings; print(settings.GEMINI_API_KEY[:10])"
```

### Issue: "Gemini API Error: Invalid API key"

**Solution:**
1. Go to https://aistudio.google.com/app/apikey
2. Generate new key
3. Update `.env` file
4. Restart backend

### Issue: "Rate limit exceeded"

**Solution:**
- API automatically waits and retries
- Free tier: 60 calls/minute
- Paid tier: Higher limits
- See [Google Pricing](https://ai.google.dev/pricing)

### Issue: "Empty response from Gemini API"

**Solution:**
1. Verify API key is valid
2. Check internet connection
3. Ensure Generative Language API is enabled
4. Try again (temporary service issue)

### Issue: PDF upload returns error

**Solution:**
1. Ensure file is valid PDF
2. File size < 100MB
3. Contains extractable text
4. Try: `pdftotext resume.pdf` to test

## Gemini Models Available

The project uses **Gemini 1.5 Pro** by default:

```python
# From config.py
GEMINI_MODEL: str = "gemini-1.5-pro"
```

**Available Models:**
- `gemini-1.5-pro` - Recommended (better reasoning, 128K context)
- `gemini-1.5-flash` - Faster, cheaper (1M token context)
- `gemini-pro` - Legacy (not recommended)

To switch models, update `backend/.env`:
```
GEMINI_MODEL=gemini-1.5-flash
```

## Cost Estimation

**Free Tier:**
- 15 requests/minute
- 500 requests/day
- $0 cost

**Paid Tier (after free credits exhausted):**
- Gemini 1.5 Pro: ~$0.075 per 1M input tokens, $0.3 per 1M output tokens
- Gemini 1.5 Flash: ~$0.0075 per 1M input tokens, $0.03 per 1M output tokens

**Example Costs:**
- Resume analysis: ~$0.001
- Interview question generation: ~$0.002
- Interview evaluation: ~$0.001
- Career recommendation: ~$0.003

## Security Best Practices

### 1. Never Commit API Keys

```bash
# Verify .env is in .gitignore
grep ".env" .gitignore

# Should show:
# .env
# .env.local
# .env.*.local
```

### 2. Use Environment Variables

```python
# ✅ CORRECT
GEMINI_API_KEY=settings.GEMINI_API_KEY

# ❌ INCORRECT
GEMINI_API_KEY="AIzaSyD..."  # Never hardcode!
```

### 3. Rotate Keys Regularly

```bash
# In Google AI Studio
1. Go to https://aistudio.google.com/app/apikey
2. Delete old key
3. Generate new key
4. Update .env
```

### 4. Monitor API Usage

```bash
# Check quota at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
```

## Advanced Configuration

### Custom Parameters

Edit `backend/app/core/config.py`:

```python
GEMINI_MODEL: str = "gemini-1.5-pro"      # Model to use
GEMINI_MAX_TOKENS: int = 2048             # Max response length
```

### Disable AI Features (Fallback)

If API key not configured, system uses fallback responses:

```python
if not settings.GEMINI_API_KEY:
    # Uses hardcoded fallback responses
    return fallback_recommendations
```

## Deployment with Gemini

### Production Environment Variables

```bash
# .env.production
DATABASE_URL=postgresql://...
SECRET_KEY=<strong-random-key>
GEMINI_API_KEY=<production-api-key>
CORS_ORIGINS=https://yourdomain.com
```

### Docker Deployment

```dockerfile
# Dockerfile includes google-generativeai in requirements
RUN pip install -r requirements.txt
```

### API Key Management (Recommended)

Use cloud secret management:

**AWS Secrets Manager:**
```python
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='gemini-api-key')
GEMINI_API_KEY = secret['SecretString']
```

**Google Cloud Secret Manager:**
```bash
gcloud secrets create gemini-api-key --data-file=-
```

## Resources

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python SDK](https://ai.google.dev/tutorials/python_quickstart)
- [Pricing](https://ai.google.dev/pricing)
- [Models](https://ai.google.dev/models)

## Support

For issues:
1. Check logs: `http://localhost:8000/docs`
2. Review error messages
3. Check API key validity
4. See troubleshooting section above
