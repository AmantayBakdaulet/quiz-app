from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from models.user_answer import UserAnswer


class UserAnswerRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_answer(self, user_id: UUID, question_id: UUID, given_answer: Dict[str, Any], is_correct: bool):
        answer = UserAnswer(user_id=user_id, question_id=question_id, given_answer=given_answer, is_correct=is_correct)
        self.session.add(answer)
        self.session.commit()
        self.session.refresh(answer)
        return answer

    def get_correct_answer_percentage(self, question_id: UUID) -> float:
        total_answers = self.session.query(UserAnswer).filter(
            UserAnswer.question_id == question_id
        ).count()
        correct_answers = self.session.query(UserAnswer).filter(
            UserAnswer.question_id == question_id,
            UserAnswer.is_correct == True
        ).count()
        if total_answers == 0:
            return 0
        percentage = (correct_answers / total_answers) * 100
        return round(percentage)
    
    def get_by_user_and_question(self, user_id: UUID, question_id: UUID) -> Optional[UserAnswer]:
        return self.session.query(UserAnswer).filter(
            UserAnswer.user_id == user_id,
            UserAnswer.question_id == question_id
        ).first()
    
    def get_all_by_question(self, question_id: UUID) -> List[UserAnswer]:
        return self.session.query(UserAnswer).filter(UserAnswer.question_id == question_id).all()
