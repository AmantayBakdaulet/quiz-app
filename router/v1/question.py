from typing import Any, Dict, List
from uuid import UUID


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.language import get_language
from dependencies.user import get_user_id
from schemas.question import QuestionInput, QuestionOutput, QuestionUpdate
from schemas.user_answer import SubmitOutput
from services.question_service import QuestionService


router = APIRouter()

@router.post("/", status_code=201, response_model=QuestionOutput)
async def create_question(
    data: QuestionInput, 
    session: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    _service = QuestionService(session, None)
    return _service.create(data)

@router.get("/", status_code=200, response_model=List[QuestionOutput])
async def get_questions(
    session: Session = Depends(get_db), 
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuestionService(session, language)
    return _service.get_all()

@router.get("/by-quiz/{quiz_id}", status_code=200, response_model=List[QuestionOutput])
async def get_questions_by_quiz(
    quiz_id: UUID, 
    session: Session = Depends(get_db), 
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuestionService(session, language)
    return _service.get_all_by_quiz(quiz_id)

@router.get("/by-id/{_id}", status_code=200, response_model=QuestionOutput)
async def get_question(
    _id: UUID,
    session: Session = Depends(get_db), 
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuestionService(session, language)
    return _service.get(_id)

@router.delete("/{_id}", status_code=204)
async def delete_question(
    _id: UUID, 
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_db)
):
    _service = QuestionService(session, None)
    return _service.delete(_id)

@router.put("/{_id}", status_code=200, response_model=QuestionInput)
async def update_question(
    _id: UUID, 
    data: QuestionUpdate,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_db)
):
    _service = QuestionService(session, None)
    return _service.update(_id, data)

@router.post("/{_id}/submit", response_model=SubmitOutput)
def submit_answer(
    _id: UUID, 
    given_answer: Dict[str, Any], 
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_db)
):
    _service = QuestionService(session, None)
    return _service.submit_answer(user_id, _id, given_answer)
