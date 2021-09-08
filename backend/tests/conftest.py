from src import settings


def pytest_unconfigure(config):
    print('Starting cleanup...')
