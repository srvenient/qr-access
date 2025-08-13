from typing import Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.api.role.domain.role_models import Role


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str | None = Field(default=None, nullable=True)
    last_name: str | None = Field(default=None, nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128, nullable=False)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    """
    Represents a user in the system.
    Inherits from SQLModel to ensure it can be used with SQLAlchemy ORM.

    :since: 0.0.1
    """
    __tablename__ = "users"

    id: str = Field(nullable=False, primary_key=True)
    hashed_password: str

    # Foreign key to the roles table
    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")

    # Relationship to the RoleAggregateRoot
    role: Optional["Role"] = Relationship()


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: str


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
