# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

DevPrepLab is a full-stack coding interview preparation platform with timed challenges, automated testing, and performance tracking. The system uses isolated Docker containers for secure code execution.

## Development Commands

### Frontend (Next.js)
```bash
cd frontend
npm install              # Install dependencies
npm run dev             # Development server (http://localhost:3000)
npm run build           # Production build
npm run lint            # Run ESLint
```

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv    # Create virtual environment
source .venv/bin/activate  # Activate (use `.venv/bin/Activate.ps1` on Windows)
pip install -r requirements.txt  # Install dependencies
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Development server

# Database migrations
alembic revision --autogenerate -m "description"  # Create migration
alembic upgrade head    # Apply migrations
alembic downgrade -1    # Rollback one migration

# Testing
pytest                  # Run all tests
pytest app/tests/test_auth.py  # Run specific test file
pytest -v              # Verbose output
pytest -k "test_name"  # Run tests matching pattern
```

### Docker Services
```bash
docker-compose up -d              # Start all services (postgres, redis, backend)
docker-compose down               # Stop all services
docker-compose logs -f backend    # Follow backend logs
docker-compose ps                 # Check service status
```

Note: PostgreSQL runs on port 5433 (not default 5432) to avoid conflicts with local installations.

## Architecture

### System Design
This is a three-layer architecture with isolated code execution:

**Client Layer**: Next.js 14 (App Router) with TypeScript, Monaco Editor for code editing, Zustand for state management, and Tailwind CSS for styling.

**API Gateway Layer**: FastAPI backend handling authentication (JWT), request validation, rate limiting, and routing to service layer.

**Service Layer**: Modular services for problems, submissions, authentication, and statistics. The execution service manages Docker-based sandboxed code runners.

**Data Layer**: PostgreSQL for persistent storage (users, problems, test cases, submissions, statistics) and Redis for caching, rate limiting, and session management.

### Code Execution Flow
1. User submits code → Frontend sends to `/api/submissions`
2. Backend validates auth, rate limits, and sanitizes input
3. Execution service creates isolated Docker container with resource limits
4. Code runs against test cases with timeout/memory constraints
5. Results (stdout, stderr, execution time, memory) collected
6. Submission stored in database with results
7. User statistics updated asynchronously

### Key Security Measures
- Docker containers with CPU, memory, and time limits
- Network isolation in execution sandbox
- No file system access during code execution
- Input sanitization and validation
- Per-user rate limiting

## Project Structure

### Backend (`backend/`)
- `app/main.py`: FastAPI application entry point
- `app/api/endpoints/`: API route handlers (auth, problems, submissions, stats)
- `app/core/`: Configuration, database connection, security utilities
- `app/models/`: SQLAlchemy ORM models (User, Problem, Submission, TestCase, UserStatistic)
- `app/schemas/`: Pydantic validation schemas for request/response
- `app/services/`: Business logic layer
- `app/utils/`: Utility functions (code runner, validators)
- `app/tests/`: Test files using pytest
- `alembic/`: Database migration scripts

### Frontend (`frontend/`)
- `app/`: Next.js App Router pages and API routes
  - `problems/`: Problem browsing and details
  - `practice/[id]/`: Code editor and submission interface
  - `dashboard/`: User statistics
  - `history/`: Past submissions
- `components/`: React components
  - `editor/`: CodeEditor (Monaco), LanguageSelector, TestResults
  - `timer/`: Countdown timer for timed challenges
  - `problems/`: ProblemCard, ProblemList, DifficultyBadge
  - `stats/`: StatsOverview, ProgressChart
  - `ui/`: Reusable UI components
- `lib/`: Utilities and state management
  - `api/`: API client functions
  - `store/`: Zustand stores (authStore, editorStore)
- `types/`: TypeScript type definitions

## Database

### Environment Configuration
Local development uses port 5433 for PostgreSQL (configured in docker-compose.yml). The `app/core/config.py` automatically adjusts connection settings based on ENVIRONMENT variable.

### Models
- **User**: Authentication and profile data
- **Problem**: Challenge descriptions, difficulty, category, constraints
- **TestCase**: Input/output pairs for validation (visible and hidden)
- **Submission**: User code, language, status, execution metrics
- **UserStatistic**: Aggregated performance metrics per user

### Migrations
Database schema changes are managed via Alembic. Always create migrations after modifying models in `app/models/`.

## Technology Stack

### Frontend
- Next.js 14 with App Router
- TypeScript (strict mode enabled)
- Tailwind CSS v4
- Monaco Editor for code editing
- Zustand for state management
- Axios for HTTP requests
- Recharts for data visualization

### Backend
- FastAPI with Python 3.9+
- SQLAlchemy 2.0 ORM
- PostgreSQL 15
- Redis for caching
- Pydantic for validation
- JWT authentication (python-jose)
- Docker SDK for code execution
- pytest for testing

## API Structure

Base URL: `http://localhost:8000/api`

### Endpoints
- `/auth/*`: User registration, login, token refresh
- `/problems/*`: Problem CRUD, random selection, test cases
- `/submissions/*`: Code submission, results, history
- `/stats/*`: User statistics, leaderboard, progress tracking

## Path Aliases

Frontend uses `@/*` for imports (maps to project root):
```typescript
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api/client'
```

## Important Notes

- Backend `.env` file contains database credentials and SECRET_KEY (never commit with real secrets)
- Code execution requires Docker daemon running and accessible
- Monaco Editor loads lazily to improve initial page load
- PostgreSQL port 5433 (not 5432) is used to avoid local DB conflicts
- Test database is separate: `test_devpreplab`
