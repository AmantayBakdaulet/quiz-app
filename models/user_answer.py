import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, UUID, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship

from dependencies.database import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    given_answer = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    attempted_at = Column(DateTime, default=datetime.now)
    question = relationship("Question", back_populates="user_answers")
