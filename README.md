# AI Internship & Placement Intelligence Platform (MVP)

This repository contains a modular MVP for an AI-powered student placement readiness platform.

## Overview

- Frontend: Next.js 15 + TypeScript + Tailwind CSS
- Backend: FastAPI + SQLAlchemy + PostgreSQL + JWT auth
- AI stack: local LLM placeholder + sentence-transformers + ChromaDB integration stub
- Deployment: Docker Compose with Postgres, backend, frontend, and ChromaDB

## Folder Structure

- `backend/` - FastAPI backend application
- `frontend/` - Next.js frontend application
- `docker-compose.yml` - local stack definition

## Backend Features

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/resume/upload`
- `GET /api/resume/analysis`
- `POST /api/interview/generate`
- `POST /api/interview/evaluate`
- `POST /api/internships`
- `GET /api/internships`
- `GET /api/career/recommendations`
- `GET /api/dashboard`

## Setup

### 1. Install dependencies

From the repository root:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
cd ../frontend
npm install
```

### 2. Configure environment

Copy environment templates:

```bash
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env.local
```

Update `backend/.env` with a strong `SECRET_KEY`.

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Local development

### Start backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start frontend

```bash
cd frontend
npm run dev
```

## Deployment Guide

1. Build Docker images:

```bash
docker compose build
```

2. Start services:

```bash
docker compose up -d
```

3. Verify app:

- `http://localhost:3000` for frontend
- `http://localhost:8000/docs` for backend OpenAPI docs

## Notes

- Resume analysis currently uses local PDF extraction and a simple ATS scoring heuristic.
- Interview preparation and career advising are implemented as MVP stubs ready for LLM integration.
- ChromaDB is included as a service in Docker Compose and can be extended for semantic search and document retrieval.
