from typing import Optional

from pydantic import BaseModel


class NewUser(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    pk: str
    username: str
    email: str
    created_at: str


class UserCredentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
