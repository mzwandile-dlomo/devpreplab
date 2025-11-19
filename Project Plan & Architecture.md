# Coding Interview Trainer - Project Plan & Architecture

## Project Overview
A full-stack application that helps developers prepare for technical interviews with timed coding challenges, automated testing, and performance tracking.

---

## Core Features

### 1. Problem Management
- Random problem selection from curated database
- Difficulty levels: Easy, Medium, Hard
- Categories: Arrays, Strings, Trees, Graphs, Dynamic Programming, etc.
- Problem details: description, examples, constraints, test cases

### 2. Coding Environment
- In-browser code editor with syntax highlighting
- Multiple language support (Python, JavaScript, Java, C++)
- Timer with visual countdown
- Real-time feedback

### 3. Solution Validation
- Automated test case execution
- Performance metrics: time complexity, space complexity
- Edge case validation
- Memory usage tracking

### 4. Progress Tracking
- Personal statistics dashboard
- Success rate by difficulty/category
- Time spent per problem
- Streak tracking
- Historical performance graphs

---

## Technology Stack

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Code Editor**: Monaco Editor (VS Code's editor)
- **State Management**: React Context + Zustand
- **Charts**: Recharts
- **HTTP Client**: Axios

### Backend (Python)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Code Execution**: Docker containers (isolated execution)
- **Authentication**: JWT tokens
- **Validation**: Pydantic

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **API Gateway**: FastAPI with CORS
- **Database**: PostgreSQL 15
- **Caching**: Redis (for rate limiting, session management)
- **Code Execution Sandbox**: Docker with resource limits

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Next.js Frontend (Port 3000)               │ │
│  │  • Problem List UI    • Code Editor (Monaco)           │ │
│  │  • Timer Component    • Stats Dashboard                │ │
│  │  • Authentication     • Results Display                │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             FastAPI Backend (Port 8000)                │ │
│  │  • RESTful Endpoints  • JWT Auth Middleware            │ │
│  │  • Request Validation • Rate Limiting                  │ │
│  │  • Error Handling     • Logging                        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   SERVICE LAYER          │  │   EXECUTION LAYER        │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ Problem Service    │  │  │  │ Code Runner        │  │
│  │ User Service       │  │  │  │ (Docker Sandbox)   │  │
│  │ Submission Service │  │  │  │ • Python Exec      │  │
│  │ Stats Service      │  │  │  │ • JS Exec          │  │
│  └────────────────────┘  │  │  │ • Resource Limits  │  │
└──────────────────────────┘  │  │ • Timeout Control  │  │
                              │  └────────────────────┘  │
                              └──────────────────────────┘
                │                           │
                │                           │
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   DATA LAYER             │  │   CACHE LAYER            │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ PostgreSQL         │  │  │  │ Redis              │  │
│  │ • users            │  │  │  │ • Sessions         │  │
│  │ • problems         │  │  │  │ • Rate Limits      │  │
│  │ • submissions      │  │  │  │ • Leaderboard      │  │
│  │ • test_cases       │  │  │  └────────────────────┘  │
│  │ • statistics       │  │  └──────────────────────────┘
│  └────────────────────┘  │
└──────────────────────────┘
```

---

## Database Schema

### Users Table
```sql
users
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
```

### Problems Table
```sql
problems
- id (UUID, PK)
- title (VARCHAR)
- description (TEXT)
- difficulty (ENUM: easy, medium, hard)
- category (VARCHAR)
- time_limit (INTEGER) -- seconds
- memory_limit (INTEGER) -- MB
- created_at (TIMESTAMP)
```

### Test Cases Table
```sql
test_cases
- id (UUID, PK)
- problem_id (UUID, FK)
- input (JSON)
- expected_output (JSON)
- is_hidden (BOOLEAN)
- weight (INTEGER)
```

### Submissions Table
```sql
submissions
- id (UUID, PK)
- user_id (UUID, FK)
- problem_id (UUID, FK)
- code (TEXT)
- language (VARCHAR)
- status (ENUM: passed, failed, error, timeout)
- execution_time (INTEGER) -- milliseconds
- memory_used (INTEGER) -- KB
- submitted_at (TIMESTAMP)
```

### User Statistics Table
```sql
user_statistics
- id (UUID, PK)
- user_id (UUID, FK)
- problems_solved (INTEGER)
- total_attempts (INTEGER)
- success_rate (DECIMAL)
- avg_time (INTEGER)
- streak_days (INTEGER)
- last_activity (TIMESTAMP)
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh access token

### Problems
- `GET /api/problems` - List all problems (with filters)
- `GET /api/problems/random` - Get random problem
- `GET /api/problems/:id` - Get specific problem details
- `GET /api/problems/:id/test-cases` - Get visible test cases

### Submissions
- `POST /api/submissions` - Submit code for testing
- `GET /api/submissions/:id` - Get submission result
- `GET /api/submissions/user/:userId` - Get user's submission history

### Statistics
- `GET /api/stats/user/:userId` - Get user statistics
- `GET /api/stats/leaderboard` - Get global leaderboard
- `GET /api/stats/progress/:userId` - Get detailed progress data

---

## Code Execution Flow

1. **User submits code** → Frontend sends to `/api/submissions`
2. **Backend validates** → Check auth, rate limits, input sanitization
3. **Create sandbox** → Spin up isolated Docker container
4. **Execute code** → Run against test cases with timeout/memory limits
5. **Collect results** → Capture stdout, stderr, execution time, memory
6. **Store submission** → Save to database with results
7. **Return response** → Send results back to frontend
8. **Update stats** → Async task updates user statistics

### Security Measures
- Resource limits (CPU, memory, time)
- Network isolation in Docker containers
- No file system access
- Input sanitization
- Rate limiting per user

---

## Frontend Pages & Components

### Pages
1. **Home** (`/`) - Landing page with features
2. **Problems** (`/problems`) - Browse all problems
3. **Practice** (`/practice/:id`) - Coding environment
4. **Dashboard** (`/dashboard`) - User statistics
5. **History** (`/history`) - Past submissions

### Key Components
- `ProblemCard` - Display problem preview
- `CodeEditor` - Monaco editor wrapper with language selector
- `Timer` - Countdown timer with alerts
- `TestResults` - Display test case results
- `StatsChart` - Visualize progress over time
- `DifficultyBadge` - Styled difficulty indicator

---

## Development Phases

### Phase 1: Core Infrastructure (Week 1-2)
- Set up Next.js project with TypeScript
- Create FastAPI backend structure
- Configure PostgreSQL database
- Implement basic authentication
- Create database models and migrations

### Phase 2: Problem System (Week 3)
- Build problem CRUD operations
- Create test case management
- Implement random problem selection
- Design problem display UI

### Phase 3: Code Execution (Week 4)
- Set up Docker sandbox environment
- Implement code runner for Python
- Add timeout and resource limits
- Create submission validation logic

### Phase 4: Frontend Development (Week 5)
- Integrate Monaco Editor
- Build timer component
- Create submission flow
- Design results display

### Phase 5: Statistics & Analytics (Week 6)
- Implement stats tracking
- Create dashboard visualizations
- Build progress charts
- Add leaderboard

### Phase 6: Polish & Deploy (Week 7)
- Add multiple language support
- Implement error handling
- Performance optimization
- Write documentation
- Deploy to production

---

## Environment Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15
- Redis

### Local Development
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Docker services
docker-compose up -d
```

---

## Testing Strategy

### Frontend
- Unit tests: Jest + React Testing Library
- E2E tests: Playwright
- Component tests for editor, timer, results

### Backend
- Unit tests: pytest
- Integration tests: API endpoint testing
- Code execution tests: Validate sandbox security

---

## Performance Considerations

- Code editor lazy loading
- Problem list pagination
- Redis caching for frequent queries
- Connection pooling for database
- Docker container reuse for executions
- Debounced code validation

---

## Future Enhancements

- Real-time collaborative coding
- Video explanations for solutions
- AI-powered hints system
- Mock interview mode with interviewer simulation
- Company-specific problem sets
- Peer code review system
- Mobile app (React Native)

---

## Success Metrics

- Average time per problem completion
- User retention rate
- Problems solved per session
- Code execution success rate
- System response time < 200ms
- Sandbox creation time < 3s