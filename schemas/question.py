from enum import Enum
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel

from .quiz import QuizOutput


class QuestionTypeEnum(str, Enum):
    SINGLE = "SingleChoice"
    FILL = "FillTheGap"
    MULTI = "MultiChoice"
    MATCH = "Matching"

class QuestionBase(BaseModel):
    type: QuestionTypeEnum
    title: str
    content: Dict[str, Any]

    class Config:
        from_attributes = True

class QuestionInput(QuestionBase):
    quiz_id: UUID
    correct_answer: Dict[str, Any]

class QuestionUpdate(BaseModel):
    type: Optional[QuestionTypeEnum] = None
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    quiz_id: Optional[UUID] = None
    correct_answer: Optional[Dict[str, Any]] = None

class QuestionOutput(QuestionBase):
    id: UUID
    quiz_id: UUID
    quiz: QuizOutput

class QuestionOutputWithAnswer(QuestionBase):
    id: UUID
    correct_answer: Dict[str, Any]
    quiz_id: UUID
    quiz: QuizOutput
