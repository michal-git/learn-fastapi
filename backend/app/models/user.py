from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER)
