

from mongoengine import DoesNotExist
from passlib.context import CryptContext

from . import models, schemas

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
