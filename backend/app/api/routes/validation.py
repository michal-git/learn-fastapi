from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlmodel import select

from app.api.deps import SessionDep
from app.models.user import User


router = APIRouter(tags=["validation"])


class ValidationResponse(BaseModel):
    field: str
    value: str
    is_unique: bool
    message: str


@router.get(
    "/validate/email",
    response_model=ValidationResponse,
    summary="Validate email uniqueness",
    description="Checks if the provided email is already registered. Returns a structured JSON response indicating whether the email is available.",
)
def validate_email(
    session: SessionDep,
    email: str = Query(..., description="Email to check uniqueness"),
):
    user = session.exec(select(User).where(User.email == email)).first()
    if user:
        return ValidationResponse(
            field="email",
            value=email,
            is_unique=False,
            message="Email is already taken.",
        )
    return ValidationResponse(
        field="email", value=email, is_unique=True, message="Email is available."
    )


@router.get(
    "/validate/username",
    response_model=ValidationResponse,
    summary="Validate username uniqueness",
    description="Checks if the provided username is already registered. Returns a structured JSON response indicating whether the username is available.",
)
def validate_username(
    session: SessionDep,
    username: str = Query(..., description="Username to check uniqueness"),
):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        return ValidationResponse(
            field="username",
            value=username,
            is_unique=False,
            message="Username is already taken.",
        )
    return ValidationResponse(
        field="username",
        value=username,
        is_unique=True,
        message="Username is available.",
    )
