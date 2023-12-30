from pydantic import BaseModel

from backend.models.roles import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: Role = Role.USER
