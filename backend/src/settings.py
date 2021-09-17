from .utils import get_env

# security
SECRET_KEY = get_env('SECRET_KEY')  # generated with openssl -hex 32
JWT_ALGORITHM = get_env('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION = get_env('JWT_TOKEN_EXPIRATION', 30)
ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', ['*'])

# database
DB_NAME = get_env('DB_NAME')
DB_USERNAME = get_env('DB_USERNAME')
DB_PASSWORD = get_env('DB_PASSWORD')
DB_HOST = get_env('DB_HOST')
DB_PORT = get_env('DB_PORT', type_cast=int)

# testing
TEST_DB_NAME = get_env('TEST_DB_NAME', 'test')

# misc
USERNAME_MAX_LENGTH = get_env('USERNAME_MAX_LENGTH', 20)
USERNAME_MIN_LENGTH = get_env('USERNAME_MIN_LENGTH', 3)
