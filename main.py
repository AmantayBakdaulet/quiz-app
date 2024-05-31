from fastapi import FastAPI

from dependencies.database import engine, Base
from dependencies.language import get_language
from router.v1 import quiz, question, user_balance


Base.metadata.create_all(bind=engine)

app = FastAPI(
    include_in_schema=True,
    openapi_url = '/documents',
    docs_url = '/docs',
    redoc_url = '/redoc',
    version = "1.0",
    title = 'QUIZ APP API Documentation'
)

app.include_router(quiz.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(question.router, prefix="/questions", tags=["questions"])
app.include_router(user_balance.router, prefix="/balance", tags=["balances"])

@app.middleware("http")
async def handle_translation(request, call_next):
    language = get_language(request.headers.get("accept-language"))
    request.state.language = language
    response = await call_next(request)
    return response
