from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.deps import UserAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.user_models import User, UserCreate
from app.core import security


async def register_user(
        user_create: UserCreate,
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
):
    """
    Register a new user in the system.
    """
    # Check if the user already exists
    existing_user = await repository.find_async(email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Hash the password before saving
    user_create.hashed_password = security.get_password_hash(user_create.password)

    # Save the new user
    user = User(**user_create.model_dump())

    try:
        await repository.find_async(email=user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def authenticate_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
):
    user_db = await repository.find_async(email=form_data.username)
    if not user_db or not security.verify_password(form_data.password, user_db.hashed_password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    pass
