from pydantic import BaseModel, Field, conlist
from typing import List, Optional, Union
from uuid import UUID, uuid4
from enum import Enum

from app.schemas.fill_gap_sentence import FillGapSentence
from app.schemas.multiple_choice_question import MultipleChoiceQuestion


class ExerciseType(str, Enum):
    FILL_GAP = "fill-gap"
    MULTIPLE_CHOICE = "multiple-choice"


class ExerciseBase(BaseModel):
    title: str
    description: Optional[str] = None
    exercise_type: ExerciseType


class FillGapExerciseCreate(ExerciseBase):
    exercise_type: ExerciseType = ExerciseType.FILL_GAP
    fill_gap_sentences: List[FillGapSentence] = Field(..., min_items=1)


class MultipleChoiceExerciseCreate(ExerciseBase):
    exercise_type: ExerciseType = ExerciseType.MULTIPLE_CHOICE
    multiple_choice_questions: List[MultipleChoiceQuestion] = Field(..., min_items=1)


ExerciseCreate = Union[FillGapExerciseCreate, MultipleChoiceExerciseCreate]


class Exercise(ExerciseBase):
    id: UUID = Field(default_factory=uuid4)
    fill_gap_sentences: Optional[List[FillGapSentence]] = None
    multiple_choice_questions: Optional[List[MultipleChoiceQuestion]] = None
