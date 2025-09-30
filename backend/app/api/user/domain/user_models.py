import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.api.role.domain.role_models import Role


class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False, unique=True)

    role_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="roles.id",
        nullable=True
    )

    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    role: Optional["Role"] = Relationship(back_populates="users")

    hashed_password: str = Field(nullable=False)

    created_at: datetime.datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: datetime.datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_column_kwargs={"onupdate": datetime.datetime.now(datetime.timezone.utc)}
    )


class UserPublic(UserBase):
    id: uuid.UUID
