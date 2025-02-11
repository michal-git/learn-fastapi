from typing import List
from uuid import UUID

from fastapi import HTTPException
from app.db.inmemory import EXERCISES
from app.schemas.exercise import Exercise, ExerciseCreate, ExerciseUpdate


def get_exercises() -> List[Exercise]:
    return EXERCISES


def get_exercise(exercise_id: UUID) -> Exercise:
    exercise = next((e for e in EXERCISES if e.id == exercise_id), None)
    if exercise is None:
        raise HTTPException(
            status_code=404, detail=f"Exercise with ID {exercise_id} not found."
        )

    return exercise


def create_exercise(exercise_data: ExerciseCreate) -> Exercise:
    new_exercise = Exercise(**exercise_data.model_dump())
    EXERCISES.append(new_exercise)
    return new_exercise


def update_exercise(exercise_id: UUID, update_data: ExerciseUpdate) -> Exercise:
    exercise = get_exercise(exercise_id)
    updated_exercise = exercise.model_copy(
        update=update_data.model_dump(exclude_unset=True)
    )

    index = EXERCISES.index(exercise)
    EXERCISES[index] = updated_exercise
    return updated_exercise


def delete_exercise(exercise_id: UUID) -> None:
    exercise = next((e for e in EXERCISES if e.id == exercise_id), None)
    if exercise is None:
        raise HTTPException(
            status_code=404, detail=f"Exercise with ID {exercise_id} not found."
        )

    EXERCISES.remove(exercise)
