import os


class EnvironmentError(Exception):
    pass


def get_env(key, default=None) -> str:
    try:
        return os.environ[key]
    except KeyError:
        if default:
            return default
        else:
            raise EnvironmentError(
                f'The value for {key} has not been set and no default is present.'
            )
