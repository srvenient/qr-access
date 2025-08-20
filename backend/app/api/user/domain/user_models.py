from datetime import datetime, timezone
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.api.role.domain.role_models import Role


class DocumentType(str, Enum):
    ID_CARD = "ID_Card"  # CC
    FOREIGN_ID = "Foreign_ID"  # CE
    PASSPORT = "Passport"  # PASAPORTE
    CITIZEN_CARD = "Citizen_Card"  # TI
    TAX_ID = "Tax_ID"  # NIT


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)

    document_type: DocumentType | None = Field(default=None, nullable=True)
    document_number: str | None = Field(default=None, max_length=50, nullable=True)
    full_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20, nullable=True)

    is_active: bool = Field(default=True, nullable=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128, nullable=False)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20, nullable=True)


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

    id: UUID = Field(nullable=False, primary_key=True)

    password_hash: str = Field(max_length=128, nullable=False)

    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")
    role: Optional["Role"] = Relationship()

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # override updated_at automatically
    def touch(self):
        self.updated_at = datetime.now(timezone.utc)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    pass


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
