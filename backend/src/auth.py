

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from mongoengine import DoesNotExist
from passlib.context import CryptContext

from . import models, schemas, settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def authenticate(credentials: schemas.UserCredentials) -> models.User:
    try:
        user = models.User.objects.get(username=credentials.username)
    except DoesNotExist:
        return None
    if verify_password(credentials.password, user.password):
        return user
    else:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
