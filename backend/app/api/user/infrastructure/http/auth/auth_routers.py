from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import UserAggregateRepositoryDep, RefreshTokenAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.application import auth_services
from app.api.user.domain.auth_models import Token, RefreshToken
from app.api.user.domain.user_models import UserCreate, User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(
        user_create: UserCreate,
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
):
    return await auth_services.register_user(user_create, repository)


@router.post("/login", response_model=auth_services.Token)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep,
        refresh_token_repository: SQLAlchemyAggregateRootRepository[RefreshToken] = RefreshTokenAggregateRepositoryDep
) -> Token:
    return await auth_services.authenticate_user(response, form_data, user_repository, refresh_token_repository)


@router.post("/refresh", response_model=auth_services.Token)
async def refresh_token(
        request: Request,
        response: Response,
        refresh_token_repository: SQLAlchemyAggregateRootRepository[RefreshToken] = RefreshTokenAggregateRepositoryDep
) -> Token:
    return await auth_services.refresh_token(request, response, refresh_token_repository)


@router.post("/logout", status_code=200)
async def logout(
        request: Request,
        response: Response,
        refresh_token_repository: SQLAlchemyAggregateRootRepository[RefreshToken] = RefreshTokenAggregateRepositoryDep
) -> dict:
    return await auth_services.logout(request, response, refresh_token_repository)
