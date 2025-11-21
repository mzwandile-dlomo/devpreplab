
from fastapi import APIRouter

from app.api.endpoints import auth, problems, test_cases, submissions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
api_router.include_router(test_cases.router, tags=["test_cases"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
