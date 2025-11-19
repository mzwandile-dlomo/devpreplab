
import uuid
from sqlalchemy import Column, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import ForeignKey

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    input = Column(JSON, nullable=False)
    expected_output = Column(JSON, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)
    weight = Column(Integer, default=1, nullable=False)
