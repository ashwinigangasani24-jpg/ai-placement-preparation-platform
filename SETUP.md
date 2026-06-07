# Project Setup & Startup Guide

## Prerequisites

- Python 3.10+ 
- Node.js 18+
- PostgreSQL 14+ (local or Docker)
- npm or yarn

## Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (already provided)
# Edit .env if needed - especially DATABASE_URL and SECRET_KEY

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: `http://localhost:8000`
API Docs available at: `http://localhost:8000/docs`

### 2. Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend dev server
npm run dev
```

Frontend will run on: `http://localhost:3000`

### 3. Database Setup

PostgreSQL should be running on `localhost:5432`.

If using Docker for just the database:

```bash
docker run -d \
  --name placement-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=placement \
  -p 5432:5432 \
  postgres:15
```

## Docker Compose (Full Stack)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Database: `localhost:5432`

## Testing the Application

1. **Register a new account**: `http://localhost:3000/register`
2. **Login**: `http://localhost:3000/login`
3. **View Dashboard**: `http://localhost:3000/dashboard`
4. **Upload Resume**: `http://localhost:3000/resume`
5. **Practice Interview**: `http://localhost:3000/interview`
6. **Track Internships**: `http://localhost:3000/internships`
7. **Career Advisor**: `http://localhost:3000/career`

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/placement
SECRET_KEY=your_super_secret_key_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000
CHROMA_HOST=http://localhost:8001
LLM_MODEL_NAME=llama-3
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Common Issues & Fixes

### Issue: "Failed to connect to database"
**Solution**: Ensure PostgreSQL is running and DATABASE_URL is correct.

### Issue: "CORS error"
**Solution**: Check that frontend URL matches CORS_ORIGINS in backend .env.

### Issue: "401 Unauthorized"
**Solution**: Ensure you are logged in and the auth token is stored in localStorage.

### Issue: "API response 404"
**Solution**: Check that frontend is using correct API URL (http://localhost:8000/api).

### Issue: "Port already in use"
**Solution**: Change port in uvicorn command or Next.js PORT env variable.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Resume Analysis
- `POST /api/resume/upload` - Upload PDF resume
- `GET /api/resume/analysis` - Get latest resume analysis

### Interview Preparation
- `POST /api/interview/generate` - Generate interview questions
- `POST /api/interview/evaluate` - Evaluate interview answers

### Internship Tracking
- `POST /api/internships` - Add internship application
- `GET /api/internships` - Get user internships

### Career Advisor
- `GET /api/career/recommendations` - Get career recommendations

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### System
- `GET /health` - Health check
- `GET /` - API info

## Production Deployment

See `DEPLOYMENT.md` for production deployment instructions.

## Support

For issues, check:
- Backend logs: `http://localhost:8000/docs`
- Frontend console: Browser DevTools (F12)
- Error messages in application UI
