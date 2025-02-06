from typing import List
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException

from app.schemas.truefalse_question import TrueFalseQuestion
from app.db.inmemory import TRUE_FALSE_QUESTIONS

router = APIRouter(tags=["truefalse_questions"])


@router.post("/questions/tf/", response_model=TrueFalseQuestion)
def create_truefalse_question(question: TrueFalseQuestion):
    question.id = uuid4()
    TRUE_FALSE_QUESTIONS.append(question)
    return question


@router.get("/questions/tf/", response_model=List[TrueFalseQuestion])
def get_truefalse_questions():
    return TRUE_FALSE_QUESTIONS


@router.get("/questions/tf/{q_id}", response_model=TrueFalseQuestion)
def get_truefalse_question(q_id: UUID):
    question = [q for q in TRUE_FALSE_QUESTIONS if q.id == q_id]
    if question:
        return question[0]

    raise HTTPException(
        status_code=404, detail=f"True/False question with ID {q_id} not found"
    )
