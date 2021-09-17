from . import models, schemas


def user_create(new_user: schemas.NewUser) -> models.User:
    return models.User(
        **new_user.dict()
    ).save()
