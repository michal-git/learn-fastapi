from fastapi import APIRouter

from app.schemas.user import UserCreate, UserRead
from app.api.deps import SessionDep
from app.services.user_service import register_user


router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Register a new user",
)
def register(user_data: UserCreate, session: SessionDep):
    return register_user(user_data, session)
