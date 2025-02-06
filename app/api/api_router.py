from fastapi import APIRouter

from app.api.routes import truefalse_questions

api_router = APIRouter()
api_router.include_router(truefalse_questions.router)
