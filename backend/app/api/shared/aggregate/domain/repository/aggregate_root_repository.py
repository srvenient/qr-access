from abc import ABC, abstractmethod
from typing import TypeVar, Optional, List, Generic

from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)


class AggregateRootRepository(ABC, Generic[T]):
    """
    Abstract base class for all Aggregate Root repositories in the domain layer.

    This interface defines the essential synchronous CRUD operations for working
    with Aggregate Roots in a Domain-Driven Design (DDD) context.

    Concrete implementations should handle the persistence logic (e.g., SQL, NoSQL, in-memory).

    :param T: The type of Aggregate Root this repository manages.
    :since: 0.0.1
    """

    @abstractmethod
    def delete_sync(self, _id: str) -> bool:
        """
        Remove an Aggregate Root from the repository by its unique identifier.

        :param _id: The unique identifier of the Aggregate Root to delete.
        :return: True if the Aggregate Root was found and deleted, False otherwise.
        """
        pass

    @abstractmethod
    def delete_all_sync(self) -> None:
        """
        Remove all Aggregate Roots from the repository.

        :return: None
        """
        pass

    @abstractmethod
    def delete_and_retrieve_sync(self, _id: str) -> Optional[T]:
        """
        Remove an Aggregate Root from the repository and return the deleted instance.

        :param _id: The unique identifier of the Aggregate Root to delete.
        :return: The deleted Aggregate Root instance, or None if it was not found.
        """
        pass

    @abstractmethod
    def exists_sync(self, _id: str) -> bool:
        """
        Check whether an Aggregate Root exists in the repository.

        :param _id: The unique identifier of the Aggregate Root to check.
        :return: True if the Aggregate Root exists, False otherwise.
        """
        pass

    @abstractmethod
    def find_sync(self, _id: str) -> Optional[T]:
        """
        Retrieve an Aggregate Root by its unique identifier.

        :param _id: The unique identifier of the Aggregate Root.
        :return: The Aggregate Root instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def find_all_sync(self) -> List[T]:
        """
        Retrieve all Aggregate Roots stored in the repository.

        :return: A list containing all Aggregate Roots.
        """
        pass

    @abstractmethod
    def find_ids_sync(self) -> List[str]:
        """
        Retrieve the unique identifiers of all Aggregate Roots in the repository.

        :return: A list of Aggregate Root IDs.
        """
        pass

    @abstractmethod
    def save_sync(self, aggregate_root: T) -> None:
        """
        Persist an Aggregate Root to the repository.
        If the Aggregate Root already exists, it should be updated.

        :param aggregate_root: The Aggregate Root instance to persist.
        :return: None
        """
        pass