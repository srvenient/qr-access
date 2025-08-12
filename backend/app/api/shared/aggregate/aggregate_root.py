from abc import ABC, abstractmethod


class AggregateRoot(ABC):
    """
    Base class for all Aggregate Roots in the aggregate.
    Contains the essential attributes and behaviors
    to represent an aggregate root in a DDD context.

    :since: 0.0.1
    """

    __slots__ = ("_id",)

    def __init__(self, _id: str) -> None:
        """
        Creates a new AggregateRoot with the specified id.

        :param _id: Unique identifier of the AggregateRoot.
        :raises ValueError: If id is not a non-empty string.
        """
        if not isinstance(_id, str) or not _id.strip():
            raise ValueError("AggregateRoot id must be a non-empty string")
        self._id: str = _id

    @property
    def id(self) -> str:
        """
        Returns the unique and immutable identifier of the AggregateRoot.
        """
        return self._id

    def __eq__(self, other) -> bool:
        """
        Aggregate roots are considered equal if their ids are equal.
        """
        return isinstance(other, AggregateRoot) and self._id == other._id

    def __hash__(self) -> int:
        """
        Hash is based solely on the id to maintain identity consistency.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self._id}')>"

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Must return a serializable representation of the aggregate.
        This enforces each aggregate to define its own serialization.
        """
        pass
