import jwt

from typing import Any

from fastapi import Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.user.domain.auth_models import Token
from app.api.user.domain.user_models import User
from app.core import security
from app.core.config import settings


class AuthService:
    def __init__(self, user_repo: SQLAlchemyAggregateRootRepository[User]):
        self.user_repo = user_repo

    @staticmethod
    def issue_access_token(user: User) -> Token:
        access_token, jti = security.create_access_token(
            subject=str(user.id),
            aud=security.ACCESS_AUD,
            ttl=security.timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            extra={"role": user.role.name} if user.role else None
        )
        return Token(access_token=access_token)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repo.find_async(email=email)

    async def authenticate_user(
            self,
            response: Response,
            form_data: OAuth2PasswordRequestForm
    ) -> dict[str, str]:
        form_password = form_data.password

        user: User = await self.get_user_by_email(form_data.username)

        # Avoid timing attacks by using a constant-time comparison
        if not user:
            # If user is not found, we still call verify_password to mitigate timing attacks
            security.verify_password(
                form_password,
                security.DUMMY_HASHED_PASSWORD
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify the password is correct
        if not security.verify_password(form_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check if the user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        # Generate JWT token
        access_token = AuthService.issue_access_token(user)

        # Set the token in an HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=access_token.access_token,
            httponly=True,
            secure=True if settings.ENV == "production" else False,
            samesite="strict" if settings.ENV == "production" else "lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return {"detail": "Login successful"}
