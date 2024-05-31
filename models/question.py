import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, JSON, String

from dependencies.database import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    correct_answer = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    quiz = relationship("Quiz", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question")
