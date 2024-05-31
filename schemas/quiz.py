from uuid import UUID

from pydantic import BaseModel


class QuizBaze(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True

class QuizInput(BaseModel):
    title: str

class QuizOutput(QuizBaze):
    pass

class QuizCompletionResponse(BaseModel):
    user_score: int
