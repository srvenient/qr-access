from typing import TypeVar, Optional, List, Type
from app.api.shared.aggregate.domain.aggregate_root import AggregateRoot
from app.api.shared.aggregate.domain.repository.async_aggregate_root_repository import AsyncAggregateRootRepository

T = TypeVar("T", bound=AggregateRoot)


class SQLAggregateRootRepository(AsyncAggregateRootRepository[T]):
    """
    A synchronous SQL-based repository implementation for managing aggregate roots.

    This repository extends the asynchronous repository interface but provides
    synchronous (blocking) operations. It is intended for environments where
    async I/O is not required or where blocking operations are acceptable.

    Type Parameters:
        T (AggregateRoot): The type of aggregate root managed by this repository.

    Attributes:
        session: A SQLAlchemy-like session used for executing queries and transactions.
        model_class (Type[T]): The class of the aggregate root entity.
    """

    def __init__(self, session, model_class: Type[T]):
        """
        Initialize the repository with a database session and model class.

        Args:
            session: A SQLAlchemy-like session instance used for database operations.
            model_class (Type[T]): The class of the aggregate root entity.
        """
        self.session = session
        self.model_class = model_class

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
        aggregate_root = self.session.get(self.model_class, _id)
        if aggregate_root:
            self.session.delete(aggregate_root)
            self.session.commit()
            return True
        return False

    def delete_all_sync(self) -> None:
        """
        Delete all aggregate roots from the repository.

        Note:
            This is a blocking method and may be expensive for large datasets.
        """
        self.session.query(self.model_class).delete()
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
        aggregate_root = self.session.get(self.model_class, _id)
        if aggregate_root:
            self.session.delete(aggregate_root)
            self.session.commit()
            return aggregate_root
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
        return self.session.query(self.model_class).filter_by(id=_id).count() > 0

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
        return self.session.get(self.model_class, _id)

    def find_all_sync(self) -> List[T]:
        """
        Retrieve all aggregate roots.

        Returns:
            List[T]: A list containing all aggregate roots.

        Note:
            This is a blocking method.
        """
        return self.session.query(self.model_class).all()

    def find_ids_sync(self) -> List[str]:
        """
        Retrieve the IDs of all aggregate roots.

        Returns:
            List[str]: A list containing all aggregate root IDs.

        Note:
            This is a blocking method.
        """
        return [ar.id for ar in self.session.query(self.model_class).all()]

    def save_sync(self, aggregate_root: T) -> None:
        """
        Save an aggregate root to the repository.

        Args:
            aggregate_root (T): The aggregate root to persist.

        Note:
            This is a blocking method.
        """
        self.session.add(aggregate_root)
        self.session.commit()