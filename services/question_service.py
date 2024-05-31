from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.question import QuestionInput, QuestionOutput, QuestionUpdate
from schemas.quiz import QuizOutput
from schemas.user_answer import SubmitOutput
from repositories.question_repository import QuestionRepository
from repositories.quiz_repository import QuizRepository
from repositories.user_answer_repository import UserAnswerRepository
from translation_service import TranslationService


class QuestionService:

    def __init__(self, session: Session, language: Optional[str]):
        self.repository = QuestionRepository(session)
        self.language = language
        self.quiz_repository = QuizRepository(session)
        self.user_answer_repository = UserAnswerRepository(session)

    def create(self, data: QuestionInput) -> QuestionOutput:
        if self.repository.question_exists_by_title(data.title):
            raise HTTPException(status_code=400, detail="Question already exists")
        
        if not self.quiz_repository.qiuz_exists_by_id(data.quiz_id):
            raise HTTPException(status_code=400, detail="Quiz not found")
        
        question = self.repository.create(data)

        return QuestionOutput(**question.model_dump(exclude_none=True))

    def get_all_by_quiz(self, quiz_id: UUID) -> List[QuestionOutput]:
        questions = self.repository.get_all_by_quiz(quiz_id)
        return self._map_and_translate(questions=questions, language=self.language)

    def get_all(self) -> List[QuestionOutput]:
        questions = self.repository.get_all()
        return self._map_and_translate(questions=questions, language=self.language)
    
    def get(self, question_id: UUID):
        question = self.repository.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return self._map_and_translate(questions=[question], language=self.language)[0]

    def delete(self, _id: UUID) -> bool:
        if not self.repository.question_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Question not found")
        question = self.repository.get_by_id(_id)
        return self.repository.delete(question)

    def update(self, _id: UUID, data: QuestionUpdate):
        if not self.repository.question_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Question not found")
        
        if not self.quiz_repository.qiuz_exists_by_id(data.quiz_id):
            raise HTTPException(status_code=400, detail="Quiz not found")
        
        question = self.repository.get_by_id(_id)
        updated_question = self.repository.update(question, data)
        return updated_question

    def submit_answer(self, user_id: UUID, question_id: UUID, given_answer: Dict[str, Any]) -> SubmitOutput:
        question = self.repository.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        is_correct = given_answer == question.correct_answer
        self.user_answer_repository.save_answer(user_id, question_id, given_answer, is_correct)

        correct_percentage = self.user_answer_repository.get_correct_answer_percentage(question_id)
        if is_correct:
            message = f"Amazing! You answered better than {correct_percentage}% of the users!"
        else:
            message = f"Unfortunately, that's incorrect."
        return SubmitOutput(is_correct=is_correct, message=message)

    @staticmethod
    def _map_and_translate(questions: List[QuestionOutput], language: str) -> List[QuestionOutput]:
        _service = TranslationService()
        return [
            QuestionOutput(
                id=question.id,
                quiz_id=question.quiz_id,
                type=question.type,
                title=_service.translate_str(target=language, content=question.title),
                content=_service.translate_dict(target=language, content=question.content),
                quiz=QuizOutput(
                    id=question.quiz.id,
                    title=_service.translate_str(target=language, content=question.quiz.title)
                )
            )
            for question in questions
        ]
