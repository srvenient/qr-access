from datetime import timezone, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.deps import UserAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.auth_models import Token
from app.api.user.domain.user_models import User, UserCreate
from app.core import security
from app.core.config import settings


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

    password_hash = security.get_password_hash(user_create.password)

    # Save the new user
    user = User.model_validate(
        user_create,
        update={"password_hash": password_hash}
    )

    await repository.save_async(user)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="User registered successfully")


async def authenticate_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        repository: SQLAlchemyAggregateRootRepository[User] = UserAggregateRepositoryDep
) -> Token:
    """
    Authenticate a user and return JWT tokens.
    """
    user_db = await repository.find_async(email=form_data.username)

    # Avoid variable time (basic protection against user enumeration)
    if not user_db or not user_db.password_hash:
        security.verify_password(form_data.password, security.DUMMY_HASHED_PASSWORD)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user_db.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    now_ = datetime.now(timezone.utc)
    if user_db.lock_until and user_db.lock_until > now_:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is locked until {user_db.lock_until.isoformat()}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not security.verify_password(form_data.password, user_db.password_hash):
        user_db.failed_attempts += 1
        if user_db.failed_attempts >= settings.FAILED_LOGIN_ATTEMPTS:
            user_db.lock_until = now_ + timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        await repository.save_async(user_db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Reset failed attempts on successful login
    user_db.failed_attempts = 0
    user_db.lock_until = None

    await repository.save_async(user_db)

    # Generate access and refresh tokens
    access_ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, access_jti = security.sign_jwt(
        str(user_db.id),
        security.ACCESS_AUD,
        access_ttl
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_ttl.total_seconds(),
        jti=access_jti
    )
