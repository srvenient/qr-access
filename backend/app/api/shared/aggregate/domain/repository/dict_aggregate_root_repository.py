from typing import Optional, TypeVar

from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot
from app.api.shared.aggregate.domain.repository.async_aggregate_root_repository import AsyncAggregateRootRepository

T = TypeVar("T", bound=AggregateRoot)


class DictAggregateRootRepository(AsyncAggregateRootRepository[T]):
    """
    In-memory implementation of AggregateRootRepository using a dictionary.
    This repository stores aggregate roots in a dictionary, allowing for fast access
    and manipulation of aggregate roots by their unique identifiers.

    :since: 0.0.1
    """

    def __init__(self) -> None:
        self._store: dict[str, T] = {}

    def delete_sync(self, _id: str) -> bool:
        """
        Deletes the current aggregate root from the repository.

        :param _id: Unique identifier of the aggregate root to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        return self._store.pop(_id, None) is not None

    def delete_all_sync(self) -> None:
        """
        Deletes all aggregate roots from the repository.

        :return: None
        """
        self._store.clear()

    def delete_and_retrieve_sync(self, _id: str) -> Optional[T]:
        """
        Deletes the current aggregate root from the repository and returns it.

        :param _id: Unique identifier of the aggregate root to delete.
        :return: The deleted aggregate root, or None if it was not found.
        """
        return self._store.pop(_id, None)

    def exists_sync(self, _id: str) -> bool:
        """
        Checks if the current aggregate root exists in the repository.

        :param _id: Unique identifier of the aggregate root to check.
        :return: True if it exists, False otherwise.
        """
        return _id in self._store

    def find_sync(self, _id: str) -> Optional[T]:
        """
        Finds an aggregate root by its ID.

        :param _id: The unique identifier of the aggregate root.
        :return: The aggregate root if found, otherwise None.
        """
        return self._store.get(_id)

    def find_all_sync(self) -> list[T]:
        """
        Retrieves all aggregate roots from the repository.

        :return: A list of all aggregate roots.
        """
        return list(self._store.values())

    def find_ids_sync(self) -> list[str]:
        """
        Finds all aggregate root IDs.

        :return: A list of all aggregate root IDs.
        """
        return list(self._store.keys())

    def save_sync(self, aggregate_root: T) -> None:
        """
        Saves the aggregate root to the repository.

        :param aggregate_root: The aggregate root to save.
        :return: None
        """
        self._store[aggregate_root.id()] = aggregate_root
