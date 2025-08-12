from abc import ABC, abstractmethod
from typing import TypeVar, Optional, List

from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)


class AggregateRootRepository(ABC):
    """
    Base class for all Aggregate Root Repositories in the domain.
    Provides the essential methods to manage aggregate roots in a DDD context.

    :since: 0.0.1
    """

    @abstractmethod
    def delete_sync(self, _id: str) -> bool:
        """
        Deletes the current aggregate root from the repository.

        :return: True if the deletion was successful, False otherwise.
        """
        pass

    @abstractmethod
    def delete_all_sync(self) -> None:
        """
        Deletes all aggregate roots from the repository.

        :return: None
        """
        pass

    @abstractmethod
    def delete_and_retrieve_sync(self, _id: str) -> Optional[T]:
        """
        Deletes the current aggregate root from the repository and returns it.

        :return: The deleted aggregate root, or None if it was not found.
        """
        pass

    @abstractmethod
    def exists_sync(self, _id: str) -> bool:
        """
        Checks if the current aggregate root exists in the repository.

        :return: True if it exists, False otherwise.
        """
        pass

    @abstractmethod
    def find_sync(self, _id: str) -> Optional[T]:
        """
        Finds an aggregate root by its ID.

        :param _id: The unique identifier of the aggregate root.
        :return: The aggregate root if found, otherwise None.
        """
        pass

    @abstractmethod
    def find_all_sync(self) -> list[T]:
        """
        Retrieves all aggregate roots from the repository.

        :return: A list of all aggregate roots.
        """
        pass

    @abstractmethod
    def find_ids_sync(self) -> list[str]:
        """
        Retrieves the IDs of all aggregate roots in the repository.

        :return: A list of aggregate root IDs.
        """
        pass

    @abstractmethod
    def save_sync(self, aggregate_root: T) -> None:
        """
        Saves the given aggregate root to the repository.
        If it already exists, it will be updated.

        :param aggregate_root: The aggregate root to save.
        :return: None
        """
        pass
