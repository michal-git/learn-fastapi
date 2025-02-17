from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from sqlalchemy import JSON, func

if TYPE_CHECKING:
    from app.models.exercise import Exercise


class MultipleChoiceQuestion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    exercise_id: UUID = Field(foreign_key="exercise.id", nullable=False)
    question: str
    choices: List[str] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    correct_index: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, nullable=False, server_default=func.now()),
    )

    # Relationship back to Exercise
    exercise: Optional["Exercise"] = Relationship(
        back_populates="multiple_choice_questions"
    )
