from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from sqlalchemy import func

if TYPE_CHECKING:
    from app.models.exercise import Exercise


class FillGapSentence(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    exercise_id: UUID = Field(foreign_key="exercise.id", nullable=False)
    sentence: str
    correct_answer: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, nullable=False, server_default=func.now()),
    )

    # Relationship back to Exercise
    exercise: Optional["Exercise"] = Relationship(back_populates="fill_gap_sentences")
