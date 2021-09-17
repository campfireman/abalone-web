from pymongo import MongoClient
from src import settings


def pytest_unconfigure(config):
    print('Starting cleanup...')
    print('Deleting database...')
    mongo_client = MongoClient(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
    )
    mongo_client.drop_database(settings.TEST_DB_NAME)
