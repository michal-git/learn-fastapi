from typing import List
from uuid import UUID
from fastapi import APIRouter, status

from app.schemas.exercise import (
    Exercise,
    ExerciseCreate,
    ExerciseUpdate,
    SentenceCreatePayload,
    SentencesUnion,
)
from app.services.exercise_service import (
    get_exercises,
    get_exercise,
    create_exercise,
    delete_exercise,
    update_exercise,
    create_sentence_for_exercise,
)
from app.api.deps import CurrentUser, SessionDep


router = APIRouter(tags=["exercise"])


@router.get(
    "/exercises/",
    response_model=List[Exercise],
    summary="List all exercises",
    description="Retrieve a list of all available exercises stored in memory.",
)
def read_exercises(current_user: CurrentUser, session: SessionDep):
    return get_exercises(current_user, session)


@router.get(
    "/exercises/{exercise_id}",
    response_model=Exercise,
    summary="Retrieve an exercise",
    description="Get an exercise by its unique identifier. Returns a 404 error if the exercise is not found.",
)
def read_exercise(exercise_id: UUID, current_user: CurrentUser, session: SessionDep):
    return get_exercise(exercise_id, current_user, session)


@router.post(
    "/exercises/",
    response_model=Exercise,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new exercise",
    description="Create a new exercise (either fill-gap or multiple-choice) ensuring at least one sentence or question is provided.",
)
def create_exercise_endpoint(
    exercise: ExerciseCreate, current_user: CurrentUser, session: SessionDep
):
    return create_exercise(exercise, current_user, session)


@router.put(
    "/exercises/{exercise_id}",
    response_model=Exercise,
    summary="Update exercise core data",
    description="Update core fields of an exercise (title, description).",
)
def update_exercise_endpoint(
    exercise_id: UUID,
    update_data: ExerciseUpdate,
    current_user: CurrentUser,
    session: SessionDep,
):
    return update_exercise(exercise_id, update_data, current_user, session)


@router.delete(
    "/exercises/{exercise_id}",
    response_model=Exercise,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an exercise",
    description="Delete an exercise by its unique identifier. Returns HTTP 204 No Content if deletion is successful.",
)
def delete_exercise_endpoint(
    exercise_id: UUID, current_user: CurrentUser, session: SessionDep
):
    return delete_exercise(exercise_id, current_user, session)


@router.post(
    "/exercises/{exercise_id}/sentences",
    response_model=SentencesUnion,
    status_code=status.HTTP_201_CREATED,
    summary="Add new Sentence(s)",
    description="Add new sentence(s) to the exercise with the specified id.",
)
def create_sentence_for_exercise_endpoint(
    exercise_id: UUID,
    payload: SentenceCreatePayload,
    current_user: CurrentUser,
    session: SessionDep,
):
    return create_sentence_for_exercise(exercise_id, payload, current_user, session)
