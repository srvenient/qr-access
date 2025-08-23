from typing import Generator, Annotated

from fastapi import Depends, HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from sqlmodel import Session
from starlette import status

from app.api.role.domain.role_models import Role
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.user_models import User
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.core.security import oauth2_scheme


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


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
) -> User:
    """
    Get the current authenticated user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience=security.ACCESS_AUD,
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise credentials_exception

    user = await repository.find_async(user_id)  # type: ignore
    if user is None or not user.is_active:
        raise credentials_exception

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]