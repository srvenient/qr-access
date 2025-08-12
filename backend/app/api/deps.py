from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session

from app.api.role.domain.role_aggregate_root import RoleAggregateRoot, Role
from app.api.shared.aggregate.domain.repository.async_aggregate_root_repository import AsyncAggregateRootRepository
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import (
    SQLAlchemyAggregateRootRepository,
)
from app.api.user.domain.user_aggregate_root import UserAggregateRoot, User
from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_role_aggregate_root_repository(
        session: SessionDep,
) -> AsyncAggregateRootRepository[RoleAggregateRoot]:
    """
    Provides an AsyncAggregateRootRepository for RoleAggregateRoot.
    """
    return SQLAlchemyAggregateRootRepository(session=session, orm_model=Role, aggregate_class=RoleAggregateRoot)


RoleAggregateRootRepositoryDep = Annotated[
    AsyncAggregateRootRepository[RoleAggregateRoot],
    Depends(get_role_aggregate_root_repository),
]


def get_user_aggregate_root_repository(
        session: SessionDep,
) -> AsyncAggregateRootRepository[UserAggregateRoot]:
    """
    Provides an AsyncAggregateRootRepository for UserAggregateRoot.
    """
    return SQLAlchemyAggregateRootRepository(session=session, orm_model=User, aggregate_class=UserAggregateRoot)


UserAggregateRootRepositoryDep = Annotated[
    AsyncAggregateRootRepository[UserAggregateRoot],
    Depends(get_user_aggregate_root_repository),
]
