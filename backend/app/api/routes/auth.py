from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserLogin, UserRead
from app.schemas.token import Token
from app.api.deps import SessionDep
from app.services.user_service import register_user
from app.services.auth_service import authenticate_user, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Register a new user",
)
def register(user_data: UserCreate, session: SessionDep):
    return register_user(user_data, session)


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticates the user and returns a JWT access token.",
)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = authenticate_user(
        user_credentials.username, user_credentials.password, session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
    )
