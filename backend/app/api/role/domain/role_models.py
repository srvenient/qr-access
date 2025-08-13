from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.api.user.domain.user_models import User


class RoleBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=255)
    description: str | None = Field(default=None, nullable=True)


class RoleCreate(RoleBase):
    pass


class RoleRegister(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)


class RoleUpdate(RoleBase):
    name: str | None = Field(default=None, max_length=255)  # type: ignore
    description: str | None = Field(default=None, nullable=True)


class Role(RoleBase, table=True):
    """
    Represents a role in the system.
    Inherits from SQLModel to ensure it can be used with SQLAlchemy ORM.

    :since: 0.0.1
    """
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, nullable=False, primary_key=True)

    users: list["User"] = Relationship(back_populates="role")


class RolePublic(RoleBase):
    id: UUID


class RolesPublic(BaseModel):
    roles: list[RolePublic]
    count: int
