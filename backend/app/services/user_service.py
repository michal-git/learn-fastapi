from typing import Optional
from fastapi import HTTPException
from sqlmodel import select
from app.schemas.user import UserCreate, UserRead
from app.api.deps import SessionDep
from app.models.user import User
from app.core.security import hash_password


def register_user(user_data: UserCreate, session: SessionDep) -> UserRead:
    existing_user = session.exec(
        select(User).where(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken.")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserRead(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=new_user.role,
    )


def get_user_by_email(email: str, session: SessionDep) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()
