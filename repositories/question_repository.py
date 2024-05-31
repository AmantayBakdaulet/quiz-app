from uuid import UUID
from typing import List, Optional, Type
from sqlalchemy.orm import Session

from models.question import Question
from schemas.question import QuestionInput, QuestionOutput, QuestionUpdate, QuestionOutputWithAnswer
from schemas.quiz import QuizOutput


class QuestionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: QuestionInput) -> QuestionOutput:
        question = Question(**data.model_dump(exclude_none=True))
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return self._map_question_to_schema_list(questions=[question])[0]
    
    def get_all(self) -> List[Optional[QuestionOutput]]:
        questions = self.session.query(Question).all()
        return self._map_question_to_schema_list(questions=questions)

    def get_all_by_quiz(self, quiz_id: UUID) -> List[Optional[QuestionOutput]]:
        questions = self.session.query(Question).filter(Question.quiz_id == quiz_id).all()
        return self._map_question_to_schema_list(questions=questions)
    
    def get_all_by_quiz_with_answer(self, quiz_id: UUID) -> List[Optional[QuestionOutputWithAnswer]]:
        questions = self.session.query(Question).filter(Question.quiz_id == quiz_id).all()
        return self._map_question_to_schema_list_w_ans(questions=questions)

    def get_by_id(self, _id: int) -> Optional[Question]:
        return self.session.query(Question).filter(Question.id == _id).first()

    def question_exists_by_id(self, _id: UUID) -> bool:
        question = self.session.query(Question).filter(Question.id==_id).first()
        return bool(question)
    
    def question_exists_by_title(self, title: str) -> bool:
        question = self.session.query(Question).filter(Question.title==title).first()
        return bool(question)

    def update(self, question: Type[Question], data: QuestionUpdate) -> QuestionOutput:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(question, key, value)
        self.session.commit()
        self.session.refresh(question)
        return QuestionInput(**question.__dict__)
    
    def delete(self, question: Type[Question]) -> bool:
        self.session.delete(question)
        self.session.commit()
        return True
    
    @staticmethod
    def _map_question_to_schema_list(questions: List[Type[Question]]) -> List[QuestionOutput]:
        return [
            QuestionOutput(
                id=question.id,
                quiz_id=question.quiz_id,
                type=question.type,
                title=question.title,
                content=question.content,
                quiz=QuizOutput(
                    id=question.quiz.id,
                    title=question.quiz.title
                )
            )
            for question in questions
        ]
    
    @staticmethod
    def _map_question_to_schema_list_w_ans(questions: List[Type[Question]]) -> List[QuestionOutputWithAnswer]:
        return [
            QuestionOutputWithAnswer(
                id=question.id,
                quiz_id=question.quiz_id,
                type=question.type,
                title=question.title,
                content=question.content,
                correct_answer=question.correct_answer,
                quiz=QuizOutput(
                    id=question.quiz.id,
                    title=question.quiz.title
                )
            )
            for question in questions
        ]
