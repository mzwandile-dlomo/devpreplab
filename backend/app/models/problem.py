
import uuid
from sqlalchemy import Column, String, Text, Enum, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum("easy", "medium", "hard", name="difficulty_enum"), nullable=False)
    category = Column(String, nullable=False)
    time_limit = Column(Integer, nullable=False)  # in seconds
    memory_limit = Column(Integer, nullable=False)  # in MB
    starter_code = Column(Text, nullable=True)  # Python starter code template
    created_at = Column(DateTime(timezone=True), server_default=func.now())
