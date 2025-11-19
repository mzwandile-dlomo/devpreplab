
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

class ProblemCreate(ProblemBase):
    pass

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
