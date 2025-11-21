import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    user_id: uuid.UUID
    problem_id: uuid.UUID
    code: str
    language: Literal["python"]  # for now we support only Python in Phase 3


class SubmissionPreview(BaseModel):
    problem_id: uuid.UUID
    code: str
    language: Literal["python"]


class SubmissionResult(BaseModel):
    status: Literal["passed", "failed", "error", "timeout"]
    stdout: str
    stderr: str
    execution_time_ms: Optional[int] = None
    memory_kb: Optional[int] = None


class SubmissionInDB(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    problem_id: uuid.UUID
    code: str
    language: str
    status: str
    execution_time: Optional[int]
    memory_used: Optional[int]
    submitted_at: datetime

    class Config:
        from_attributes = True