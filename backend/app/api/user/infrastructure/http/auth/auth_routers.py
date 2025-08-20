from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import UserAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.application import auth_services
from app.api.user.domain.user_models import UserCreate, User, UserPublic

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(
        user_create: UserCreate,
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
):
    return auth_services.register_user(user_create, repository)


@router.post("/login")
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
):
    return auth_services.authenticate_user(response, form_data, repository)
