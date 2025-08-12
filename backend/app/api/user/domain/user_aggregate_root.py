from typing import TypeVar, Type, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.api.role.domain.role_aggregate_root import RoleAggregateRoot
from app.api.shared.aggregate.aggregate_root import AggregateRoot

TU = TypeVar("TU", bound="User")


class User(SQLModel, table=True):
    """
    Represents a user in the system.
    Inherits from SQLModel to ensure it can be used with SQLAlchemy ORM.

    :since: 0.0.1
    """
    __tablename__ = "users"

    id: UUID = Field(primary_key=True, default_factory=UUID)
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    first_name: str | None = Field(default=None, nullable=True)
    last_name: str | None = Field(default=None, nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)

    # Foreign key to the roles table
    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")

    # Relationship to the RoleAggregateRoot
    role: Optional[RoleAggregateRoot] = Relationship()

    hash_password: str | None = Field(default=None, nullable=False)


class UserAggregateRoot(AggregateRoot):
    """
    Represents a user in the system.
    Inherits from AggregateRoot to ensure it has a unique identifier.

    :since: 0.0.1
    """
    __slots__ = AggregateRoot.__slots__ + (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "is_verified",
        "role",
    )

    def __init__(
            self,
            _id: str,
            username: str,
            email: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            is_active: bool = True,
            is_superuser: bool = False,
            is_verified: bool = False,
            role: Optional[RoleAggregateRoot] = None,
    ) -> None:
        super().__init__(_id)
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
        self.role = role

    def __repr__(self) -> str:
        return f"<UserAggregateRoot id={self.id}, username={self.username}, email={self.email}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "role": self.role.to_dict() if self.role else None,
        }

    @classmethod
    def from_dict(cls: Type[TU], data: dict) -> TU:
        role_data = data.get("role")
        role = RoleAggregateRoot.from_dict(role_data) if role_data else None
        return cls(
            _id=data["id"],
            username=data["username"],
            email=data["email"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            is_active=data.get("is_active", True),
            is_superuser=data.get("is_superuser", False),
            is_verified=data.get("is_verified", False),
            role=role,
        )