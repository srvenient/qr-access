from abc import ABC, abstractmethod
from typing import TypeVar, Type

T = TypeVar("T", bound="AggregateRoot")


class AggregateRoot(ABC):
    """
    Base abstract class for all Aggregate Roots in the domain layer.

    In Domain-Driven Design (DDD), an Aggregate Root is the primary entry point
    to a cluster of domain objects. It enforces invariants and ensures that
    all modifications go through it, preserving the consistency of the aggregate.

    This class defines the core identity and serialization/deserialization
    contract for aggregate roots in the system.

    :since: 0.0.1
    """

    __slots__ = ("_id",)

    def __init__(self, _id: str) -> None:
        """
        Initializes a new AggregateRoot with the specified unique identifier.

        :param _id: Unique identifier of the AggregateRoot.
        :raises ValueError: If `_id` is not a non-empty string.
        """
        if not isinstance(_id, str) or not _id.strip():
            raise ValueError("AggregateRoot id must be a non-empty string")
        self._id: str = _id

    def id(self) -> str:
        """
        Retrieves the unique identifier of the AggregateRoot.

        :return: The unique identifier as a string.
        """
        return self._id

    def __eq__(self, other) -> bool:
        """
        Checks equality based on the aggregate's unique identifier.
        """
        return isinstance(other, AggregateRoot) and self.id == other.id

    def __hash__(self) -> int:
        """
        Returns the hash of the aggregate's unique identifier.
        """
        return hash(self.id)

    def __repr__(self) -> str:
        """
        Returns a string representation of the AggregateRoot instance.
        """
        return f"<{self.__class__.__name__}(id='{self.id}')>"

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Serializes the AggregateRoot into a dictionary representation.

        This method must be implemented by subclasses to define
        how the aggregate's state should be converted to a dictionary.

        :return: Dictionary containing the aggregate's data.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """
        Deserializes a dictionary into an AggregateRoot instance.

        This method must be implemented by subclasses to define
        how an aggregate should be reconstructed from stored data.

        :param data: Dictionary containing the aggregate's data.
        :return: An instance of the AggregateRoot subclass.
        """
        pass