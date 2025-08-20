from datetime import timedelta, datetime, timezone

import jwt
import pyotp
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.OAUTH2_TOKEN_URL,
    scopes=settings.OAUTH2_SCOPES,
    auto_error=True,
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def generate_2fa_secret_key() -> str:
    return pyotp.random_base32()


def get_totp_uri(secret: str, username: str, issuer_name="qr-access") -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer_name)


def verify_2fa_token(secret: str, token: str) -> bool:
    return pyotp.TOTP(secret).verify(token, valid_window=1)  # Allow a 30-second window for token validity
