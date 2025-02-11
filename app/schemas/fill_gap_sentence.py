from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Optional


class FillGapSentenceBase(BaseModel):
    sentence: str
    correct_answer: str


class FillGapSentenceCreate(FillGapSentenceBase):
    pass


class FillGapSentenceUpdate(BaseModel):
    sentence: Optional[str] = None
    correct_answer: Optional[str] = None


class FillGapSentence(FillGapSentenceBase):
    id: UUID = Field(default_factory=uuid4)
