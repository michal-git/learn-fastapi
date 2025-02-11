from typing import List
from uuid import UUID
from fastapi import APIRouter, status

from app.schemas.exercise import Exercise, ExerciseCreate, ExerciseUpdate
from app.services.exercise_service import (
    get_exercises,
    get_exercise,
    create_exercise,
    delete_exercise,
    update_exercise,
)


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


@router.post(
    "/exercises/",
    response_model=Exercise,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new exercise",
    description="Create a new exercise (either fill-gap or multiple-choice) ensuring at least one sentence or question is provided.",
)
def create_exercise_endpoint(exercise: ExerciseCreate):
    return create_exercise(exercise)


@router.put(
    "/exercises/{exercise_id}",
    response_model=Exercise,
    summary="Update exercise core data",
    description="Update core fields of an exercise (title, description).",
)
def update_exercise_endpoint(exercise_id: UUID, update_data: ExerciseUpdate):
    return update_exercise(exercise_id, update_data)


@router.delete(
    "/exercises/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an exercise",
    description="Delete an exercise by its unique identifier. Returns HTTP 204 No Content if deletion is successful.",
)
def delete_exercise_endpoint(exercise_id: UUID):
    delete_exercise(exercise_id)
