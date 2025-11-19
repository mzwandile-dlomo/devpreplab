
from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: uuid.UUID
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
