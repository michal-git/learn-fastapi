from fastapi import APIRouter

from app.api.routes import exercise

api_router = APIRouter()
api_router.include_router(exercise.router)
