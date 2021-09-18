from typing import Optional

from pydantic import BaseModel

from . import models


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


class Game(BaseModel):
    pk: str
    black: str
    white: str
    starting_formation: int
    created_at: str
