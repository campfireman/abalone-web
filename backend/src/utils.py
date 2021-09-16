import os

from mongoengine import Document
from pydantic import BaseModel


class EnvironmentError(Exception):
    pass


def get_env(key: str, default: str = None, type_cast: callable = None) -> str:
    value = None
    try:
        value = os.environ[key]
    except KeyError:
        if default:
            value = default
        else:
            raise EnvironmentError(
                f'The value for {key} has not been set and no default is present.'
            )
    return type_cast(value) if type_cast else value


def model_schema_intersection(model: Document, schema: BaseModel) -> dict:
    intersection = {}
    for key in schema.schema()['properties'].keys():
        value = getattr(model, key)
        intersection[key] = str(value) if key == 'pk' else value
    return intersection
