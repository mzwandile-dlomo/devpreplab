import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class TestCaseBase(BaseModel):
    input: Any
    expected_output: Any
    is_hidden: bool = False
    weight: int = 1


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    input: Optional[Any] = None
    expected_output: Optional[Any] = None
    is_hidden: Optional[bool] = None
    weight: Optional[int] = None


class TestCaseInDB(TestCaseBase):
    id: uuid.UUID
    problem_id: uuid.UUID

    class Config:
        from_attributes = True


class TestCasePublic(BaseModel):
    id: uuid.UUID
    input: Any
    expected_output: Any
    weight: int

    class Config:
        from_attributes = True
