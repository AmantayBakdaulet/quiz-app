from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.quiz import QuizInput, QuizOutput
from repositories.quiz_repository import QuizRepository
from repositories.question_repository import QuestionRepository
from repositories.user_answer_repository import UserAnswerRepository
from services.user_balance_service import UserBalanceService
from translation_service import TranslationService


class QuizService:

    def __init__(self, session: Session, language: Optional[str]):
        self.repository = QuizRepository(session)
        self.language = language
        self.session = session
        self.question_repository = QuestionRepository(session)
        self.user_answer_repository = UserAnswerRepository(session)
        self.user_balance_service = UserBalanceService(session)

    def create_quiz(self, data: QuizInput):
        if self.repository.quiz_exists_by_title(data.title):
            raise HTTPException(status_code=400, detail="Quiz already exists")
        return self.repository.create(data)

    def get_all(self) -> List[Optional[QuizOutput]]:
        quizzes = self.repository.get_all()
        if self.language:
            _service = TranslationService() 
            translated_quizzes = []
            for quiz in quizzes:
                quiz_dict = quiz.__dict__.copy()
                quiz_dict['title'] = _service.translate_str(target=self.language, content=quiz.title)
                translated_quizzes.append(QuizOutput(**quiz_dict))
            return translated_quizzes
        return quizzes

    def get_quiz(self, quiz_id: UUID) -> Optional[QuizOutput]:
        quiz = self.repository.get_by_id(quiz_id)
        if quiz:
            if self.language:
                _service = TranslationService()
                quiz_dict = quiz.__dict__.copy()
                quiz_dict['title'] = _service.translate_str(target=self.language, content=quiz.title)
                return QuizOutput(**quiz_dict)
            return quiz
        return None
    
    def delete(self, quiz_id: UUID) -> bool:
        if not self.repository.qiuz_exists_by_id(quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
        quiz = self.repository.get_by_id(quiz_id)
        self.repository.delete(quiz)
        return True
    
    def update(self, quiz_id: UUID, data: QuizInput) -> QuizOutput:
        if not self.repository.qiuz_exists_by_id(quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
        quiz = self.repository.get_by_id(quiz_id)
        return self.repository.update(quiz, data)

    def complete_quiz(self, user_id: UUID, quiz_id: UUID):
        questions = self.question_repository.get_all_by_quiz_with_answer(quiz_id)
        
        new_correct_answers = 0
        correct_answers = 0
        for question in questions:
            user_answers = self.user_answer_repository.get_all_by_question(question.id)

            has_previously_correct_answer = any(user_answer.is_correct for user_answer in user_answers)
            if has_previously_correct_answer and len(user_answers) != 1:
                continue

            current_answer = self.get_user_current_answer(user_id, question.id)

            if current_answer == question.correct_answer:
                new_correct_answers += 1
                correct_answers += 1
                if user_answers:
                    for user_answer in user_answers:
                        user_answer.is_correct = True
                    self.session.commit()
                else:
                    self.user_answer_repository.save_answer(user_id, question.id, current_answer, is_correct=True)

        if new_correct_answers > 0:
            balance_award = new_correct_answers * 100
            self.user_balance_service.add_balance(user_id, balance_award)

        user_score = correct_answers / len(questions) * 100

        return {
            "user_score": user_score
        }

    def get_user_current_answer(self, user_id: UUID, question_id: UUID) -> Dict[str, Any]:
        user_answer = self.user_answer_repository.get_by_user_and_question(user_id, question_id)

        if user_answer:
            return user_answer.given_answer
        else:
            raise HTTPException(status_code=404, detail="User answer not found")
