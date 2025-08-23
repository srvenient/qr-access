from datetime import timezone, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, ExpiredSignatureError
from starlette.responses import JSONResponse

from app.api.deps import UserAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.auth_models import Token
from app.api.user.domain.user_models import User, UserCreate
from app.core import security
from app.core.config import settings


def generate_tokens(user_id: str) -> tuple[Token, str, timedelta]:
    access_ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_ttl = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token, access_jti = security.sign_jwt(
        user_id, security.ACCESS_AUD, access_ttl
    )
    refresh_token_value, refresh_jti = security.sign_jwt(
        user_id, security.REFRESH_AUD, refresh_ttl
    )

    return (
        Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=access_ttl.total_seconds(),
            jti=access_jti,
        ),
        refresh_token_value,
        refresh_ttl,
    )


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
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User registered successfully"})


async def authenticate_user(
        response: Response,
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

    if user_db.is_locked():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is locked until {user_db.lock_until.isoformat()}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not security.verify_password(form_data.password, user_db.password_hash):
        user_db.register_failed_attempt(settings.FAILED_LOGIN_ATTEMPTS, settings.LOCKOUT_DURATION_MINUTES)
        await repository.save_async(user_db)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_db.reset_failed_attempts()

    await repository.save_async(user_db)

    # Generate access and refresh tokens
    token, refresh_token_value, refresh_ttl = generate_tokens(str(user_db.id))

    # Set refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token_value,
        httponly=True,
        max_age=int(refresh_ttl.total_seconds()),
        expires=int(refresh_ttl.total_seconds()),
        samesite="strict" if settings.ENV == "production" else "lax",
        secure=settings.COOKIE_SECURE  # Set to True in production with HTTPS
    )

    return token


async def refresh_token(request: Request, response: Response) -> Token:
    stored_refresh_token = request.cookies.get("refresh_token")
    if not stored_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        payload: dict = security.jwt.decode(
            stored_refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience=security.REFRESH_AUD,
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    token, new_refresh_token, refresh_ttl = generate_tokens(user_id)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(refresh_ttl.total_seconds())
    )

    return token
