from typing import List
from uuid import UUID
from fastapi import APIRouter

from app.schemas.exercise import Exercise
from app.services.exercise_service import get_exercises, get_exercise


router = APIRouter(tags=["exercises"])


@router.get(
    "/exercises/",
    response_model=List[Exercise],
    summary="List all exercises",
    description="Retrieve a list of all available exercises stored in memory.",
)
def read_exercises():
    return get_exercises()


@router.get(
    "/exercises/{exercise_id}",
    response_model=Exercise,
    summary="Retrieve an exercise",
    description="Get an exercise by its unique identifier. Returns a 404 error if the exercise is not found.",
)
def read_exercise(exercise_id: UUID):
    return get_exercise(exercise_id)
