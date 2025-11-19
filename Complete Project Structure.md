DevPrepLab/
│
├── frontend/                          # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── problems/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── practice/
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── history/
│   │   │   └── page.tsx
│   │   └── api/
│   │       └── auth/
│   │           └── [...nextauth]/
│   │               └── route.ts
│   ├── components/
│   │   ├── editor/
│   │   │   ├── CodeEditor.tsx
│   │   │   ├── LanguageSelector.tsx
│   │   │   └── TestResults.tsx
│   │   ├── timer/
│   │   │   └── Timer.tsx
│   │   ├── problems/
│   │   │   ├── ProblemCard.tsx
│   │   │   ├── ProblemList.tsx
│   │   │   ├── ProblemDetail.tsx
│   │   │   └── DifficultyBadge.tsx
│   │   ├── stats/
│   │   │   ├── StatsOverview.tsx
│   │   │   ├── ProgressChart.tsx
│   │   │   └── Leaderboard.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       └── Modal.tsx
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── problems.ts
│   │   │   ├── submissions.ts
│   │   │   └── auth.ts
│   │   ├── store/
│   │   │   ├── authStore.ts
│   │   │   └── editorStore.ts
│   │   └── utils/
│   │       ├── formatting.ts
│   │       └── validation.ts
│   ├── types/
│   │   ├── problem.ts
│   │   ├── submission.ts
│   │   └── user.ts
│   ├── public/
│   │   └── assets/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
│
├── backend/                           # FastAPI Backend
│   ├── app/
│   │   ├── main.py
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── problems.py
│   │   │       ├── submissions.py
│   │   │       └── stats.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   ├── submission.py
│   │   │   └── test_case.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   ├── submission.py
│   │   │   └── token.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── problem_service.py
│   │   │   ├── execution_service.py
│   │   │   └── stats_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── code_runner.py
│   │       └── validators.py
│   ├── docker/
│   │   └── execution/
│   │       ├── Dockerfile
│   │       └── runner.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_problems.py
│   │   └── test_execution.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── docker-compose.yml
├── .gitignore
├── .env.local
├── README.md
└── .dockerignore