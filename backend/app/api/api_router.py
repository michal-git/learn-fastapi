from fastapi import APIRouter

from app.api.routes import exercise, auth, validation

api_router = APIRouter()
api_router.include_router(exercise.router)
api_router.include_router(auth.router)
api_router.include_router(validation.router)
