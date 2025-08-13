from typing import Optional, TypeVar
from app.api.shared.aggregate.domain.repository.aggregate_root_repository import AggregateRootRepository

T = TypeVar("T")


class InMemoryAggregateRootRepository(AggregateRootRepository[T]):
    """
    In-memory implementation of an Aggregate Root Repository.

    This repository stores aggregate roots in an internal Python dictionary,
    providing fast in-memory access for CRUD operations. Each aggregate root is
    indexed by its unique identifier (string-based), enabling O(1) average-time
    lookup, insertion, and deletion.

    **Characteristics:**
    - Volatile storage: Data is lost when the process stops.
    - Thread-unsafe: Not safe for concurrent writes without external synchronization.
    - Ideal for testing, prototyping, or non-persistent use cases.

    :type T: TypeVar bound to AggregateRoot
    :since: 0.0.1
    """

    def __init__(self) -> None:
        """
        Initializes an empty in-memory store for aggregate roots.
        """
        self._store: dict[str, T] = {}

    def delete_sync(self, _id: str) -> bool:
        """
        Deletes an aggregate root by its unique identifier.

        :param _id: Unique identifier of the aggregate root to delete.
        :return: True if the deletion was successful, False if the ID was not found.
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
        Deletes an aggregate root by ID and returns it.

        :param _id: Unique identifier of the aggregate root to delete.
        :return: The deleted aggregate root instance, or None if not found.
        """
        return self._store.pop(_id, None)

    def exists_sync(self, _id: str) -> bool:
        """
        Checks whether an aggregate root with the given ID exists in the repository.

        :param _id: Unique identifier of the aggregate root to check.
        :return: True if it exists, False otherwise.
        """
        return _id in self._store

    def find_sync(self, _id: str) -> Optional[T]:
        """
        Retrieves an aggregate root by its ID.

        :param _id: Unique identifier of the aggregate root.
        :return: The aggregate root if found, otherwise None.
        """
        return self._store.get(_id)

    def find_all_sync(self) -> list[T]:
        """
        Retrieves all aggregate roots stored in the repository.

        :return: A list containing all aggregate root instances.
        """
        return list(self._store.values())

    def find_ids_sync(self) -> list[str]:
        """
        Retrieves all aggregate root identifiers stored in the repository.

        :return: A list containing all unique aggregate root IDs.
        """
        return list(self._store.keys())

    def save_sync(self, aggregate_root: T) -> None:
        """
        Saves (inserts or updates) an aggregate root in the repository.

        If an aggregate root with the same ID already exists, it will be replaced.

        :param aggregate_root: The aggregate root instance to persist.
        :return: None
        """
        self._store[aggregate_root.id()] = aggregate_root
