from typing import Annotated

import jwt
from fastapi import APIRouter, Header, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AuthServiceDep, UserAggregateRootRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.application.auth_services import AuthService
from app.api.user.domain.user_models import UserCreate, User
from app.core import security
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(
        user_create: UserCreate,
        user_repo: SQLAlchemyAggregateRootRepository[User] = UserAggregateRootRepositoryDep
):
    # Check if the user already exists
    existing_user = await user_repo.find_async(email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = security.get_password_hash(user_create.password)

    # Save the new user
    user = User.model_validate(
        user_create,
        update={"hashed_password": hashed_password}
    )

    await user_repo.save_async(user)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: AuthService = AuthServiceDep
):
    return await auth_service.authenticate_user(response, form_data)


@router.get("/validate-token")
async def validate_token(
        authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    token = authorization.split(" ")[1]

    is_valid, payload = await AuthService.validate_token(token)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "Token is valid", "payload": payload}


@router.post("/logout", status_code=204)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
