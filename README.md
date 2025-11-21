# DevPrepLab

A coding practice platform for technical interview preparation with secure code execution and real-time feedback.

## Tech Stack

### Backend
- **FastAPI** (0.104.1) - Modern Python web framework for building APIs
- **Python** (3.11+) - Primary backend language
- **PostgreSQL** (15) - Main database for storing problems, test cases, and submissions
- **SQLAlchemy** (2.0.23) - ORM for database operations
- **Alembic** (1.12.1) - Database migration tool
- **Pydantic** (2.5.0) - Data validation and settings management
- **Redis** (7) - Caching and session management
- **Docker** (7.1.0) - Containerization for secure code execution
- **python-jose** (3.3.0) - JWT token generation and validation
- **bcrypt** (4.0.1) - Password hashing

### Frontend
- **Next.js** (16.0.3) - React framework with server-side rendering
- **React** (19.2.0) - UI library
- **TypeScript** (5.x) - Type-safe JavaScript
- **Tailwind CSS** (4.x) - Utility-first CSS framework
- **Monaco Editor** (@monaco-editor/react 4.7.0) - Code editor (VS Code editor)
- **Axios** (1.13.2) - HTTP client for API calls
- **Zustand** (5.0.8) - State management
- **Recharts** (3.4.1) - Data visualization library
- **Lucide React** (0.554.0) - Icon library

### Testing
- **pytest** (7.4.3) - Python testing framework
- **pytest-asyncio** (0.21.1) - Async testing support
- **httpx** (0.25.2) - Async HTTP client for testing
- **Jest** (29.7.0) - JavaScript testing framework
- **React Testing Library** (16.1.0) - React component testing
- **@testing-library/jest-dom** (6.6.3) - Custom Jest matchers

### DevOps & Infrastructure
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline
- **Uvicorn** (0.24.0) - ASGI server for FastAPI
- **ESLint** (9.x) - JavaScript/TypeScript linting
- **Babel** - JavaScript transpilation

## Features

- Email-based authentication with JWT tokens
- Secure code execution in isolated Docker containers
- Real-time code testing against test cases
- Problem categorization by difficulty and category
- User submission tracking and history
- Anonymous practice mode (preview submissions)
- Resource limits (time and memory) for code execution

## Project Structure

```
DevPrepLab/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Configuration and security
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── tests/     # Pytest test suite
│   │   └── utils/     # Utilities (execution, etc.)
│   ├── alembic/       # Database migrations
│   └── docker/        # Docker configs for execution
├── frontend/          # Next.js frontend
│   ├── app/           # Next.js app directory
│   ├── components/    # React components
│   └── lib/           # Utilities and API client
└── .github/           # CI/CD workflows

```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15
- Docker
- Redis 7

### Quick Start

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Build Docker execution image:**
   ```bash
   make build-execution-image
   ```

3. **Run database migrations:**
   ```bash
   make db-migrate
   ```

4. **Seed initial problems:**
   ```bash
   make seed-problems
   ```

5. **Start development servers:**
   ```bash
   make dev
   ```

### Available Commands

```bash
make install               # Install all dependencies
make dev                   # Start both frontend and backend in dev mode
make backend-test          # Run backend tests
make frontend-test         # Run frontend tests
make build-execution-image # Build Docker image for code execution
make db-migrate            # Apply database migrations
make seed-problems         # Seed database with problems
```

## Authentication

DevPrepLab uses email-only accounts (no separate usernames). Authentication is done via JWT using the registered email address and password.
