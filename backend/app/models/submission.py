
import uuid
from sqlalchemy import Column, String, Text, Enum, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import ForeignKey

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    status = Column(Enum("passed", "failed", "error", "timeout", name="status_enum"), nullable=False)
    execution_time = Column(Integer)  # in milliseconds
    memory_used = Column(Integer)  # in KB
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
