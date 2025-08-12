from typing import TypeVar, Type

from sqlmodel import Field, SQLModel

from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot

TR = TypeVar("TR", bound="RoleAggregateRoot")


class Role(SQLModel, table=True):
    """
    Represents a role in the system.
    Inherits from SQLModel to ensure it can be used with SQLAlchemy ORM.

    :since: 0.0.1
    """
    __tablename__ = "roles"

    id: str = Field(primary_key=True)
    name: str = Field(nullable=False, index=True)
    description: str = Field(nullable=True)

    class Config:
        """
        Configuration for the SQLModel Role class.
        Ensures that the model is compatible with SQLAlchemy ORM.

        :since: 0.0.1
        """
        orm_mode = True


class RoleAggregateRoot(AggregateRoot):
    """
    Represents a role in the system.
    Inherits from AggregateRoot to ensure it has a unique identifier.

    :since: 0.0.1
    """

    __slots__ = AggregateRoot.__slots__ + ("name", "description")

    def __init__(self, _id: str, name: str, description: str | None = None) -> None:
        super().__init__(_id)
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f"<RoleAggregateRoot id={self.id}, name={self.name}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls: Type[TR], data: dict) -> TR:
        return cls(**data)