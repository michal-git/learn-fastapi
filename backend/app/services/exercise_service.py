from typing import Callable, List
from uuid import UUID

from sqlmodel import Session, select

from fastapi import Depends, HTTPException, status
from app.core.db import engine
from app.schemas.exercise import Exercise, ExerciseCreate, ExerciseType, ExerciseUpdate
from app.models.exercise import Exercise as ExerciseModel
from backend.app.models.fill_gap_sentence import FillGapSentence as FillGapSentenceModel
from backend.app.models.multiple_choice_question import (
    MultipleChoiceQuestion as MultipleChoiceQuestionModel,
)


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


def get_exercises(session: Session = Depends(get_session)) -> List[Exercise]:
    exercises_model = session.exec(select(ExerciseModel)).all()
    return [to_exercise_schema(e) for e in exercises_model]


def get_exercise(
    exercise_id: UUID, session: Session = Depends(get_session)
) -> Exercise:
    exercise_model = session.get(ExerciseModel, exercise_id)

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )

    return to_exercise_schema(exercise_model)


def create_exercise(
    exercise_data: ExerciseCreate, session: Session = Depends(get_session)
) -> Exercise:
    exercise_type = session.exec(
        select(ExerciseType).where(ExerciseType.name == exercise_data.type.value)
    ).first()

    if not exercise_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported exercise type: '{exercise_data.type.value}'.",
        )

    new_exercise = ExerciseModel(
        teacher_id=exercise_data.teacher_id,  # TODO: Use current user id
        exercise_type_id=exercise_type.id,
        title=exercise_data.title,
        description=exercise_data.description,
    )

    session.add(new_exercise)
    session.commit()
    session.refresh(new_exercise)

    handler = get_exercise_handler(exercise_data.type)
    handler(session, new_exercise.id, exercise_data)

    session.commit()
    return to_exercise_schema(new_exercise)


def update_exercise(
    exercise_id: UUID,
    update_data: ExerciseUpdate,
    session: Session = Depends(get_session),
) -> Exercise:
    exercise_model = session.get(ExerciseModel, exercise_id)

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(exercise_model, key, value)

    session.add(exercise_model)
    session.commit()
    session.refresh(exercise_model)

    return to_exercise_schema(exercise_model)


def delete_exercise(
    exercise_id: UUID, session: Session = Depends(get_session)
) -> Exercise:
    exercise = get_exercise(exercise_id)
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )

    session.delete(exercise)
    session.commit()
    return exercise


def to_exercise_schema(model: ExerciseModel) -> Exercise:
    return Exercise(
        id=model.id,
        title=model.title,
        description=model.description,
        type=ExerciseType(model.exercise_type),
        fill_gap_sentences=model.fill_gap_sentences,
        multiple_choice_questions=model.multiple_choice_questions,
    )


def get_exercise_handler(
    exercise_data_type: ExerciseType,
) -> Callable[[Session, ExerciseModel], None]:
    """
    Returns the appropriate function for handling exercise-specific related data.
    """
    if exercise_data_type == ExerciseType.FILL_GAP:
        return handle_fill_gap_exercise
    elif exercise_data_type == ExerciseType.MULTIPLE_CHOICE:
        return handle_multiple_choice_exercise
    else:
        raise ValueError(f"Unsupported exercise type: {exercise_data_type}")


def handle_fill_gap_exercise(
    session: Session, exercise_id: UUID, exercise_data: ExerciseCreate
):
    for sentence in exercise_data.fill_gap_sentences:
        fill_gap_sentence = FillGapSentenceModel(
            exercise_id=exercise_id,
            text=sentence.sentence,
            correct_answer=sentence.correct_answer,
        )
        session.add(fill_gap_sentence)


def handle_multiple_choice_exercise(
    session: Session,
    exercise_id: UUID,
    exercise_data: ExerciseCreate,
):
    for question in exercise_data.multiple_choice_questions:
        multiple_choice_question = MultipleChoiceQuestionModel(
            exercise_id=exercise_id,
            question_text=question.question,
            choices=question.choices,
            correct_choice_index=question.correct_choice_index,
        )
        session.add(multiple_choice_question)
