from typing import Callable, List
from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from fastapi import HTTPException, status
from app.schemas.exercise import (
    Exercise,
    ExerciseCreate,
    ExerciseType,
    ExerciseUpdate,
    SentenceCreate,
    SentenceCreatePayload,
    SentenceCreateUnion,
    SentencesUnion,
)
from app.models.exercise import (
    Exercise as ExerciseModel,
    ExerciseType as ExerciseTypeModel,
)
from app.api.deps import CurrentUser, SessionDep
from app.models.fill_gap_sentence import FillGapSentence as FillGapSentenceModel
from app.models.multiple_choice_question import (
    MultipleChoiceQuestion as MultipleChoiceQuestionModel,
)
from app.schemas.fill_gap_sentence import FillGapSentence, FillGapSentenceCreate
from app.schemas.multiple_choice_question import (
    MultipleChoiceQuestion,
    MultipleChoiceQuestionCreate,
)


def get_exercises(current_user: CurrentUser, session: SessionDep) -> List[Exercise]:
    exercise_models = session.exec(
        select(ExerciseModel)
        .where(ExerciseModel.owner_id == current_user.id)
        .options(
            selectinload(ExerciseModel.exercise_type),
            selectinload(ExerciseModel.fill_gap_sentences),
            selectinload(ExerciseModel.multiple_choice_questions),
        )
    ).all()

    return [to_exercise_schema(e) for e in exercise_models]


def get_exercise(
    exercise_id: UUID, current_user: CurrentUser, session: SessionDep
) -> Exercise:
    exercise_model = session.exec(
        select(ExerciseModel)
        .where(
            ExerciseModel.id == exercise_id, ExerciseModel.owner_id == current_user.id
        )
        .options(
            selectinload(ExerciseModel.exercise_type),
            selectinload(ExerciseModel.fill_gap_sentences),
            selectinload(ExerciseModel.multiple_choice_questions),
        )
    ).first()

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found for the current user.",
        )

    return to_exercise_schema(exercise_model)


def create_exercise(
    exercise_data: ExerciseCreate, current_user: CurrentUser, session: SessionDep
) -> Exercise:
    exercise_type = session.exec(
        select(ExerciseTypeModel).where(
            ExerciseTypeModel.name == exercise_data.type.value
        )
    ).first()

    if not exercise_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported exercise type: '{exercise_data.type.value}'.",
        )

    new_exercise = ExerciseModel(
        owner_id=current_user.id,
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
    current_user: CurrentUser,
    session: SessionDep,
) -> Exercise:
    exercise_model = session.exec(
        select(ExerciseModel).where(
            ExerciseModel.id == exercise_id, ExerciseModel.owner_id == current_user.id
        )
    ).first()

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found for the current user.",
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(exercise_model, key, value)

    session.add(exercise_model)
    session.commit()
    session.refresh(exercise_model)

    return to_exercise_schema(exercise_model)


def delete_exercise(
    exercise_id: UUID, current_user: CurrentUser, session: SessionDep
) -> Exercise:
    exercise_model = session.exec(
        select(ExerciseModel).where(
            ExerciseModel.id == exercise_id, ExerciseModel.owner_id == current_user.id
        )
    ).first()

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )

    session.delete(exercise_model)
    session.commit()
    return to_exercise_schema(exercise_model)


def to_exercise_schema(model: ExerciseModel) -> Exercise:
    return Exercise(
        id=model.id,
        title=model.title,
        description=model.description,
        type=ExerciseType(model.exercise_type.name) if model.exercise_type else None,
        fill_gap_sentences=(
            [
                to_fill_gap_sentence_schema(sentence)
                for sentence in model.fill_gap_sentences
            ]
            if model.fill_gap_sentences
            else []
        ),
        multiple_choice_questions=(
            [
                to_multiple_choice_question_schema(question)
                for question in model.multiple_choice_questions
            ]
            if model.multiple_choice_questions
            else []
        ),
    )


def to_fill_gap_sentence_schema(model: FillGapSentenceModel) -> FillGapSentence:
    return FillGapSentence(
        id=model.id, sentence=model.sentence, correct_answer=model.correct_answer
    )


def to_multiple_choice_question_schema(
    model: MultipleChoiceQuestionModel,
) -> MultipleChoiceQuestion:
    return MultipleChoiceQuestion(
        id=model.id,
        question=model.question,
        choices=model.choices,
        correct_index=model.correct_index,
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
            sentence=sentence.sentence,
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
            question=question.question,
            choices=question.choices,
            correct_choice_index=question.correct_choice_index,
        )
        session.add(multiple_choice_question)


def create_sentence_for_exercise(
    exercise_id: UUID,
    payload: SentenceCreatePayload,
    current_user: CurrentUser,
    session: SessionDep,
) -> SentencesUnion:
    sentences = payload.sentences

    exercise_model = session.exec(
        select(ExerciseModel).where(
            ExerciseModel.id == exercise_id, ExerciseModel.owner_id == current_user.id
        )
    ).first()

    if exercise_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )

    created_sentences_schema = dispatch_sentence_creation(
        exercise_model.type, exercise_id, sentences, session
    )

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating sentences: {str(e)}",
        )

    return created_sentences_schema


def create_fill_gap_sentences(
    exercise_id: UUID, sentences: List[FillGapSentenceCreate], session: Session
) -> List[FillGapSentenceModel]:
    created_models = []
    for sentence in sentences:
        new_fill_gap_sentence = FillGapSentenceModel(
            exercise_id=exercise_id,
            sentence=sentence.sentence,
            correct_answer=sentence.correct_answer,
        )
        session.add(new_fill_gap_sentence)
        created_models.append(new_fill_gap_sentence)
    return created_models


def create_multiple_choice_sentences(
    exercise_id: UUID, sentences: List[MultipleChoiceQuestionCreate], session: Session
) -> List[MultipleChoiceQuestionModel]:
    created_models = []
    for question in sentences:
        new_multiple_choice_question = MultipleChoiceQuestionModel(
            exercise_id=exercise_id,
            question=question.question,
            choices=question.choices,
            correct_choice_index=question.correct_choice_index,
        )
        session.add(new_multiple_choice_question)
        created_models.append(new_multiple_choice_question)
    return created_models


def dispatch_sentence_creation(
    exercise_type: ExerciseType,
    exercise_id: UUID,
    sentences: List[SentenceCreateUnion],
    session: SessionDep,
) -> SentencesUnion:
    if exercise_type == ExerciseType.FILL_GAP:
        if not isinstance(sentences[0], FillGapSentenceCreate):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sentence type does not match exercise type.",
            )
        created_models = create_fill_gap_sentences(exercise_id, sentences, session)
        return [to_fill_gap_sentence_schema(model) for model in created_models]

    elif exercise_type == ExerciseType.MULTIPLE_CHOICE:
        if not isinstance(sentences[0], MultipleChoiceQuestionCreate):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sentence type does not match exercise type.",
            )
        created_models = create_multiple_choice_sentences(
            exercise_id, sentences, session
        )
        return [to_multiple_choice_question_schema(model) for model in created_models]

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported exercise type."
        )
