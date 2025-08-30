from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from uuid import uuid4, UUID

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.api.user.domain.user_models import User


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    jti: str = Field(index=True, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at: datetime
    revoked: bool = Field(default=False)

    user_id: UUID = Field(foreign_key="users.id", index=True)
    user: Optional["User"] = Relationship(back_populates="refresh_tokens")


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: float | None = None
    jti: str | None = None
    ttl: float | None = None  # Time to live in seconds