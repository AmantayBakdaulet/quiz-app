from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy.orm import Session

from models.quiz import Quiz
from schemas.quiz import QuizInput, QuizOutput


class QuizRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: QuizInput) -> QuizOutput:
        quiz = Quiz(**data.model_dump(exclude_none=True))
        self.session.add(quiz)
        self.session.commit()
        self.session.refresh(quiz)
        return quiz

    def get_all(self) -> List[Optional[Quiz]]:
        return self.session.query(Quiz).all()

    def get_by_id(self, _id: int) -> Optional[Quiz]:
        return self.session.query(Quiz).filter(Quiz.id == _id).first()

    def qiuz_exists_by_id(self, _id: UUID) -> bool:
        quiz = self.session.query(Quiz).filter_by(id=_id).first()
        return quiz is not None

    def quiz_exists_by_title(self, title: str) -> bool:
        quiz = self.session.query(Quiz).filter_by(title=title).first()
        return quiz is not None

    def update(self, quiz: Type[Quiz], data: QuizInput) -> QuizOutput:
        quiz.title = data.title
        self.session.commit()
        self.session.refresh(quiz)
        return QuizOutput(**quiz.__dict__)

    def delete(self, quiz: Type[Quiz]) -> bool:
        self.session.delete(quiz)
        self.session.commit()
        return True
