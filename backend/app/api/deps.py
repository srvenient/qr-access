from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session

from app.api.role.domain.role_models import Role
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.user_models import User
from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_role_aggregate_repository(session: SessionDep) -> SQLAlchemyAggregateRootRepository[Role]:
    return SQLAlchemyAggregateRootRepository[Role](
        session=session,
        aggregate_root=Role
    )


RoleAggregateRepositoryDep = Depends(get_role_aggregate_repository)


def get_user_aggregate_repository(session: SessionDep) -> SQLAlchemyAggregateRootRepository[User]:
    return SQLAlchemyAggregateRootRepository[User](
        session=session,
        aggregate_root=User
    )


UserAggregateRepositoryDep = Depends(get_user_aggregate_repository)
