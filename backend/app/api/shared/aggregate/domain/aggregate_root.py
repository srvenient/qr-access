from abc import ABC, abstractmethod
from typing import TypeVar, Type

T = TypeVar("T", bound="AggregateRoot")


class AggregateRoot(ABC):
    """
    Base class for all Aggregate Roots in the domain.
    Contains the essential attributes and behaviors
    to represent an aggregate root in a DDD context.

    :since: 0.0.1
    """

    __slots__ = ("_id",)

    def __init__(self, _id: str) -> None:
        """
        Creates a new AggregateRoot with the specified id.

        :param _id: Unique identifier of the AggregateRoot.
        :raises ValueError: If the id is not a non-empty string.
        """
        if not isinstance(_id, str) or not _id.strip():
            raise ValueError("AggregateRoot id must be a non-empty string")
        self._id: str = _id

    def id(self) -> str:
        """
        Returns the unique identifier of the AggregateRoot.

        :return: Unique identifier of the AggregateRoot.
        """
        return self._id

    def __eq__(self, other) -> bool:
        return isinstance(other, AggregateRoot) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self.id}')>"

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Converts the AggregateRoot instance to a dictionary representation.

        :return: Dictionary containing the attributes of the AggregateRoot.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """
        Creates an instance of the AggregateRoot from a dictionary representation.

        :param data: Dictionary containing the attributes of the AggregateRoot.
        :return: An instance of the AggregateRoot.
        """
        pass