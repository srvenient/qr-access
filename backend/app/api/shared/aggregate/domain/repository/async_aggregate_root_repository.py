import asyncio
from abc import ABC
from typing import Optional, TypeVar, Generic

from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot
from app.api.shared.aggregate.domain.repository.aggregate_root_repository import AggregateRootRepository

T = TypeVar("T", bound=AggregateRoot)


class AsyncAggregateRootRepository(AggregateRootRepository[T], ABC):
    """
    Asynchronous wrapper for AggregateRootRepository methods.
    Executes the synchronous implementation in a thread pool using asyncio.to_thread.
    Do not override these methods unless you provide a fully asynchronous implementation.

    :since: 0.0.1
    """

    async def delete_async(self, _id: str) -> bool:
        """
        Deletes the aggregate root asynchronously.

        :return: True if the deletion was successful, False otherwise.
        """
        return await asyncio.to_thread(self.delete_sync, _id)

    async def delete_all_async(self) -> None:
        """
        Deletes all aggregate roots asynchronously.

        :return: True if the deletion was successful, False otherwise.
        """
        await asyncio.to_thread(self.delete_all_sync)

    async def delete_and_retrieve_async(self, _id: str) -> Optional[T]:
        """
        Deletes the aggregate root and retrieves it asynchronously.

        :param _id: Unique identifier of the aggregate root to delete.
        :return: The deleted aggregate root if found, None otherwise.
        """
        return await asyncio.to_thread(self.delete_and_retrieve_sync, _id)

    async def exists_async(self, _id: str) -> bool:
        """
        Checks if the aggregate root exists asynchronously.

        :param _id: Unique identifier of the aggregate root to check.
        :return: True if the aggregate root exists, False otherwise.
        """
        return await asyncio.to_thread(self.exists_sync, _id)

    async def find_async(self, _id) -> Optional[T]:
        """
        Finds the aggregate root by its unique identifier asynchronously.

        :param _id: Unique identifier of the aggregate root to find.
        :return: The found aggregate root if exists, None otherwise.
        """
        return await asyncio.to_thread(self.find_sync, _id)

    async def find_all_async(self) -> list[T]:
        """
        Finds all aggregate roots asynchronously.

        :return: A list of all aggregate roots.
        """
        return await asyncio.to_thread(self.find_all_sync)

    async def find_ids_async(self) -> list[str]:
        """
        Finds all aggregate root IDs asynchronously.

        :return: A list of all aggregate root IDs.
        """
        return await asyncio.to_thread(self.find_ids_sync)

    async def save_async(self, aggregate_root: T) -> None:
        """
        Saves the aggregate root asynchronously.

        :param aggregate_root: The aggregate root to save.
        :return: The saved aggregate root.
        """
        await asyncio.to_thread(self.save_sync, aggregate_root)
