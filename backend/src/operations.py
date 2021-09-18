from mongoengine import DoesNotExist

from . import auth, models, schemas


def user_get(username) -> models.User:
    return models.User.objects.get(username=username)


def user_delete(username):
    user_get(username=username).delete()
