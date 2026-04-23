from pydantic import BaseModel


class Token(BaseModel):
    """JWT token javob schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token ichidagi ma'lumotlar."""

    sub: str
    type: str


class RefreshTokenRequest(BaseModel):
    """Refresh token so'rovi."""

    refresh_token: str


class LoginRequest(BaseModel):
    """Login so'rovi (JSON body orqali)."""

    email: str
    password: str
