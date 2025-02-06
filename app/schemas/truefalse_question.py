from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from enum import Enum


class QuestionLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class TrueFalseQuestion(BaseModel):
    id: Optional[UUID] = None
    question: str = Field(..., min_length=3, max_length=300)
    is_true: bool
    levels: List[QuestionLevel]
