from typing import TypeVar, Optional, List, Type

from sqlmodel import Session

from app.api.shared.aggregate.domain.repository.async_aggregate_root_repository import AsyncAggregateRootRepository

T = TypeVar("T")
O = TypeVar("O")


class SQLAlchemyAggregateRootRepository(AsyncAggregateRootRepository[T]):
    """
     Repository implementation for managing Aggregate Roots using SQLAlchemy.

     This repository is **primarily asynchronous**, providing async methods for
     non-blocking operations in event-driven or concurrent environments.

     However, it also includes **synchronous counterparts** (methods with the
     `_sync` suffix) for scenarios where:
         - You are running code in a fully synchronous context.
         - You want to avoid `await` for quick blocking calls.
         - You are using environments without async support.

     **Important:**
         - The synchronous methods are **blocking** and should not be called
           from async event loops without running them in a separate thread or
           process.
         - For high concurrency, prefer the async methods.
     """

    def __init__(self, session: Session, orm_model: Type[O], aggregate_class: Type[T]):
        self.session = session
        self.orm_model = orm_model
        self.aggregate_class = aggregate_class

    def _to_aggregate(self, orm_obj: O) -> T:
        """Map ORM → AggregateRoot"""
        return self.aggregate_class(**orm_obj.__dict__)

    def _to_orm(self, aggregate: T) -> O:
        """Map AggregateRoot → ORM"""
        return self.orm_model(**aggregate.__dict__)

    def delete_sync(self, _id: str) -> bool:
        """
        Delete an aggregate root by its ID.

        Args:
            _id (str): Unique identifier of the aggregate root.

        Returns:
            bool: True if the deletion was successful, False otherwise.

        Note:
            This is a blocking method.
        """
        orm_obj = self.session.get(self.orm_model, _id)
        if orm_obj:
            self.session.delete(orm_obj)
            self.session.commit()
            return True
        return False

    def delete_all_sync(self) -> None:
        """
        Delete all aggregate roots from the repository.

        Note:
            This is a blocking method and may be expensive for large datasets.
        """
        self.session.query(self.orm_model).delete()
        self.session.commit()

    def delete_and_retrieve_sync(self, _id: str) -> Optional[T]:
        """
        Delete an aggregate root and return the deleted instance.

        Args:
            _id (str): Unique identifier of the aggregate root.

        Returns:
            Optional[T]: The deleted aggregate root if found, otherwise None.

        Note:
            This is a blocking method.
        """
        orm_obj = self.session.get(self.orm_model, _id)
        if orm_obj:
            self.session.delete(orm_obj)
            self.session.commit()
            return self._to_aggregate(orm_obj)
        return None

    def exists_sync(self, _id: str) -> bool:
        """
        Check if an aggregate root exists.

        Args:
            _id (str): Unique identifier of the aggregate root.

        Returns:
            bool: True if the aggregate root exists, False otherwise.

        Note:
            This is a blocking method.
        """
        return self.session.query(self.orm_model).filter_by(id=_id).count() > 0

    def find_sync(self, _id: str) -> Optional[T]:
        """
        Retrieve an aggregate root by its ID.

        Args:
            _id (str): Unique identifier of the aggregate root.

        Returns:
            Optional[T]: The aggregate root if found, otherwise None.

        Note:
            This is a blocking method.
        """
        orm_obj = self.session.get(self.orm_model, _id)
        return self._to_aggregate(orm_obj) if orm_obj else None

    def find_all_sync(self) -> List[T]:
        """
        Retrieve all aggregate roots.

        Returns:
            List[T]: A list containing all aggregate roots.

        Note:
            This is a blocking method.
        """
        orm_objs = self.session.query(self.orm_model).all()
        return [self._to_aggregate(o) for o in orm_objs]

    def find_ids_sync(self) -> List[str]:
        """
        Retrieve the IDs of all aggregate roots.

        Returns:
            List[str]: A list containing all aggregate root IDs.

        Note:
            This is a blocking method.
        """
        return [o.id for o in self.session.query(self.orm_model).all()]

    def save_sync(self, aggregate_root: T) -> None:
        """
        Save an aggregate root to the repository.

        Args:
            aggregate_root (T): The aggregate root to persist.

        Note:
            This is a blocking method.
        """
        orm_obj = self._to_orm(aggregate_root)
        self.session.add(orm_obj)
        self.session.commit()
