from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List, Optional


class MultipleChoiceQuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_index: int


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    pass


class MultipleChoiceQuestionUpdate(BaseModel):
    question: Optional[str] = None
    options: Optional[List[str]] = None
    correct_index: Optional[int] = None


class MultipleChoiceQuestion(MultipleChoiceQuestionBase):
    id: UUID = Field(default_factory=uuid4)
