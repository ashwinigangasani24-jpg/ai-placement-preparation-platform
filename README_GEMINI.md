# AI Internship & Placement Intelligence Platform
## With Google Gemini AI Integration

### 🎯 Project Overview

A full-stack web application designed to help students prepare for internships through AI-powered placement intelligence. The platform now uses **Google Gemini AI** for advanced generative features.

**Key Features:**
- ✅ **Gemini-Powered Resume Analysis** - Intelligent ATS scoring and skill extraction
- ✅ **AI Interview Preparation** - Dynamic question generation and smart evaluation
- ✅ **Personalized Career Roadmap** - Gemini-generated learning paths
- ✅ **Placement Readiness Assessment** - AI evaluation of job readiness
- ✅ **Real-time Interview Feedback** - Intelligent answer evaluation with scoring
- ✅ **Internship Tracking** - Application status and analytics
- ✅ **Professional Authentication** - Secure JWT-based login

### 🏗️ Tech Stack

**Backend:**
- FastAPI 0.112.0 - High-performance REST API
- SQLAlchemy 2.0.36 - Database ORM
- PostgreSQL 15 - Production database
- **Google Gemini AI** - Generative AI for intelligent analysis
- Pydantic 2.9.2 - Data validation
- Python 3.10+

**Frontend:**
- Next.js 15.2.4 - React framework
- React 18.3.1 - UI framework
- TypeScript 5.6.2 - Type safety
- Tailwind CSS 3.4.4 - Styling
- Node.js 18+

**Deployment:**
- Docker & Docker Compose - Containerization
- PostgreSQL with health checks
- Multi-stage builds for optimization

### 📋 MVP Features

#### 1. User Authentication
- Email/password registration
- JWT-based login
- Secure session management

#### 2. Resume Analysis (Powered by Gemini)
- PDF upload support
- **AI-powered ATS scoring** (0-100)
- **Gemini skill extraction** from resume
- **Intelligent skill gap analysis**
- **AI-generated recommendations** for improvement
- **Suggested job roles** based on profile

#### 3. Interview Preparation (Powered by Gemini)
- **AI-generated questions** based on profile and topic
- 3-step interview flow:
  - Generate personalized questions
  - Practice with answer input
  - Receive AI evaluation
- **Intelligent answer evaluation** with:
  - Automated scoring (0-100)
  - Detailed feedback
  - Improvement suggestions

#### 4. Career Guidance (Powered by Gemini)
- **Personalized learning roadmap** from Gemini
- **Recommended certifications** for target roles
- **Career trajectory planning**
- **Skill gap recommendations**
- 30-day action items

#### 5. Internship Tracker
- Add internship applications
- Track application status (Applied, Interviewing, Offered, Rejected, Accepted)
- View statistics dashboard
- Track progress over time

#### 6. Analytics Dashboard
- **Gemini-powered placement readiness score**
- ATS score from latest resume
- Latest interview performance
- Internship application statistics
- **AI placement feedback**

### 🚀 Quick Start

#### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+ (or Docker)
- Google Gemini API Key (free)

#### 1. Get Gemini API Key (2 minutes)

```bash
# Go to: https://aistudio.google.com/app/apikey
# Click "Create API Key"
# Copy the key
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env and add:
# GEMINI_API_KEY=your_key_here

# Initialize database
python init_db.py

# Start backend
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

#### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

#### 4. Test Application

1. Register: `http://localhost:3000/register`
2. Login: `http://localhost:3000/login`
3. Upload Resume: `/resume` - See Gemini AI analysis
4. Practice Interview: `/interview` - Get AI-generated questions
5. View Career Plan: `/career` - See Gemini recommendations
6. Check Dashboard: `/dashboard` - View placement readiness

### 📦 Docker Deployment

```bash
# Start all services (PostgreSQL, Backend, Frontend)
docker-compose up --build

# Services available at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Database: localhost:5432
```

### 🔧 API Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

#### Resume Analysis (Gemini)
- `POST /api/resume/upload` - Upload and analyze resume
- `GET /api/resume/analysis` - Get detailed analysis

#### Interview (Gemini)
- `POST /api/interview/generate` - Generate AI questions
- `POST /api/interview/evaluate` - Evaluate answers

#### Career (Gemini)
- `GET /api/career/recommendations` - Get personalized roadmap

#### Dashboard
- `GET /api/dashboard` - Get comprehensive statistics

#### System
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### 🤖 Gemini AI Integration

All AI features use **Google Gemini 1.5 Pro** with:

- ✅ Intelligent resume analysis
- ✅ Dynamic interview question generation
- ✅ Smart answer evaluation
- ✅ Personalized career recommendations
- ✅ Real-time rate limiting
- ✅ Automatic error handling with fallbacks

**For detailed Gemini setup, see [GEMINI_SETUP.md](GEMINI_SETUP.md)**

### 📊 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints (resume, interview, career, etc.)
│   │   ├── core/         # Configuration and security
│   │   ├── db/           # Database models
│   │   ├── schemas/      # Pydantic request/response models
│   │   ├── services/     # Gemini AI service layer
│   │   └── utils/        # Helper functions
│   ├── .env              # Environment variables
│   ├── requirements.txt   # Python dependencies
│   └── run.sh            # Startup script
│
├── frontend/
│   ├── app/              # Next.js pages
│   ├── lib/              # API client, auth context
│   ├── public/           # Static assets
│   ├── package.json      # Dependencies
│   └── tsconfig.json     # TypeScript config
│
├── docker-compose.yml     # Multi-service orchestration
├── SETUP.md              # Setup guide
├── GEMINI_SETUP.md       # Gemini API configuration
└── README.md             # This file
```

### 🔐 Security

- ✅ JWT authentication with secure tokens
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Environment variable management
- ✅ API key security (never committed)
- ✅ Rate limiting on API calls

### 📈 Scalability

- PostgreSQL for production data
- Docker for consistent deployment
- Efficient API design with async/await
- Optimized database queries
- Static asset caching
- Rate limiting for API protection

### 🧪 Testing

```bash
# Run validation script
python validate.py

# Check all endpoints
# Verify authentication
# Test database connection
# Validate CORS
```

### 📚 Documentation

- [SETUP.md](SETUP.md) - Local development setup
- [GEMINI_SETUP.md](GEMINI_SETUP.md) - Google Gemini API configuration
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [ERROR_FIXES_REPORT.md](ERROR_FIXES_REPORT.md) - Known issues and solutions
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI

### 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- AWS/GCP/Azure deployment
- Docker production setup
- Database backups
- SSL/TLS configuration
- Monitoring and logging
- Scaling strategies

### 💡 Example: Resume Analysis with Gemini

```python
# Backend processes this automatically:
from app.services.gemini import ResumeAnalysisService

analysis = ResumeAnalysisService.analyze_resume(resume_text)
# Returns:
{
    "ats_score": 78,
    "skills": ["Python", "SQL", "Docker"],
    "missing_skills": ["Kubernetes", "AWS", "System Design"],
    "recommendations": ["Add cloud deployment experience", ...],
    "recommended_roles": ["Backend Engineer Intern", ...]
}
```

### 💡 Example: Interview Question Generation

```python
# Gemini generates contextual questions:
from app.services.gemini import InterviewService

questions = InterviewService.generate_questions(
    profile="Python Developer",
    topic="Data Structures"
)
# Returns realistic, domain-specific interview questions
```

### 🌟 Key Achievements

✅ Full-stack MVP with modern architecture
✅ Google Gemini AI integration for all AI features
✅ Production-ready Docker setup
✅ Comprehensive API documentation
✅ Type-safe TypeScript frontend
✅ Secure authentication and authorization
✅ Database with proper relationships
✅ Error handling and logging
✅ Rate limiting and API protection
✅ Suitable for academic portfolio

### 📝 License

MIT License - Open source and free to use

### 👥 Contributors

- Development Team
- Google Gemini AI Integration

### 📞 Support

For issues or questions:
1. Check [SETUP.md](SETUP.md) and [GEMINI_SETUP.md](GEMINI_SETUP.md)
2. Review [ERROR_FIXES_REPORT.md](ERROR_FIXES_REPORT.md)
3. Check API documentation: `http://localhost:8000/docs`

---

**Built with ❤️ for students seeking career excellence**
