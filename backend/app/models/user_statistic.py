
import uuid
from sqlalchemy import Column, Integer, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import ForeignKey

class UserStatistic(Base):
    __tablename__ = "user_statistics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    problems_solved = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    success_rate = Column(DECIMAL, default=0.0)
    avg_time = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
