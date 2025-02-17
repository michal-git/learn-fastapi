from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, String, DateTime, Relationship
from sqlalchemy import func

from app.models.fill_gap_sentence import FillGapSentence
from app.models.multiple_choice_question import MultipleChoiceQuestion
from app.models.user import User


class ExerciseType(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))


class Exercise(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    owner_id: UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    exercise_type_id: UUID = Field(foreign_key="exercisetype.id", nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column=Column(DateTime, nullable=False, server_default=func.now()),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column=Column(
            DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
        ),
    )

    # Relationships
    owner: Optional["User"] = Relationship(back_populates="exercises")
    exercise_type: ExerciseType = Relationship(back_populates="exercises")
    fill_gap_sentences: List["FillGapSentence"] = Relationship(
        back_populates="exercise"
    )
    multiple_choice_questions: List["MultipleChoiceQuestion"] = Relationship(
        back_populates="exercise"
    )
