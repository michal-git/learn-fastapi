from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str
