from mongoengine import DoesNotExist

from . import auth, models, schemas


def user_get(username) -> models.User:
    return models.User.objects.get(username=username)


def user_create(new_user: schemas.NewUser) -> models.User:
    new_user_dict = new_user.dict()
    new_user_dict['password'] = auth.hash_password(new_user.password)
    return models.User(
        **new_user_dict
    ).save()


def user_delete(username):
    user_get(username=username).delete()
