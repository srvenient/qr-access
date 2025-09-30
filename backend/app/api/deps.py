from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session

from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.application.auth_service import AuthService
from app.api.user.domain.user_models import User
from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_user_aggregate_root_repository(session: SessionDep) -> SQLAlchemyAggregateRootRepository[User]:
    return SQLAlchemyAggregateRootRepository[User](session, User)


UserAggregateRootRepositoryDep = Depends(get_user_aggregate_root_repository)

def get_auth_service(
        user_repo: SQLAlchemyAggregateRootRepository[User] = UserAggregateRootRepositoryDep
) -> AuthService:
    return AuthService(user_repo)


AuthServiceDep = Depends(get_auth_service)
