from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: float | None = None
    jti: str | None = None