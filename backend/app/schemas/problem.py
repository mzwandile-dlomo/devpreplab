
from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime


class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    category: str
    time_limit: int
    memory_limit: int
    starter_code: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    time_limit: Optional[int] = None
    memory_limit: Optional[int] = None
    starter_code: Optional[str] = None


class ProblemInDB(ProblemBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ProblemPublic(BaseModel):
    id: uuid.UUID
    title: str
    difficulty: str
    category: str

    class Config:
        from_attributes = True
