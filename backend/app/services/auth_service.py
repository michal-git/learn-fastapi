from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app.api.deps import SessionDep
from app.core.security import verify_password
from app.models.user import User
from app.services.user_service import get_user_by_email
from app.core.config import ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(email: str, password: str, session: SessionDep) -> Optional[User]:
    user = get_user_by_email(email, session)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
