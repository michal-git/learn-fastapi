from typing import List
from uuid import UUID

from fastapi import HTTPException
from app.db.inmemory import EXERCISES
from app.schemas.exercise import Exercise


def get_exercises() -> List[Exercise]:
    return EXERCISES


def get_exercise(exercise_id: UUID) -> Exercise:
    exercise = next((e for e in EXERCISES if e.id == exercise_id), None)
    if exercise is None:
        raise HTTPException(
            status_code=404, detail=f"Exercise with ID {exercise_id} not found."
        )
    return exercise
