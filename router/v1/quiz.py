from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.language import get_language
from dependencies.user import get_user_id
from schemas.quiz import QuizInput, QuizOutput, QuizCompletionResponse
from services.quiz_service import QuizService


router = APIRouter()

@router.post("/", response_model=QuizOutput)
async def create_quiz(
    data: QuizInput, 
    session: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuizService(session, None)
    return _service.create_quiz(data)

@router.get("/", response_model=List[QuizOutput])
async def get_all(
    session: Session = Depends(get_db), 
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id)
) ->  List[QuizOutput]:
    _service = QuizService(session, language)
    return _service.get_all()

@router.get("/{_id}", response_model=Optional[QuizOutput])
async def get_quiz(
    _id: UUID, 
    session: Session = Depends(get_db), 
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuizService(session, language)
    return _service.get_quiz(_id)

@router.put("/{_id}", response_model=QuizOutput)
async def update_quiz(
    _id: UUID, 
    data: QuizInput, 
    session: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuizService(session, None)
    return _service.update(_id, data)

@router.delete("/{_id}", status_code=204)
async def delete_quiz(
    _id: UUID, 
    session: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id)
):
    _service = QuizService(session, None)
    return _service.delete(_id)

@router.post("/complete_quiz/{quiz_id}", response_model=QuizCompletionResponse)
def complete_quiz(
    quiz_id: UUID,
    session: Session = Depends(get_db), 
    user_id: UUID = Depends(get_user_id),
    language: str = Depends(get_language)
):
    service = QuizService(session, language)
    result = service.complete_quiz(user_id, quiz_id)
    return QuizCompletionResponse(
        user_score=result["user_score"]
    )
