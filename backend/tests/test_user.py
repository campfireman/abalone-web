from fastapi import status
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from src import auth, enums, forms, models
from src import operations as op
from src import schemas, settings
from src.api import app

client = TestClient(app)

disconnect()
connect(
    db=settings.TEST_DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    authentication_source='admin',
)

TEST_USER = schemas.NewUser(
    username='peterpopper',
    email='peter@popper.com',
    password='password',
)
TEST_USER2 = schemas.NewUser(
    username='peterpopper2',
    email='peter@popper2.com',
    password='password',
)


def test_created_user_valid():
    response = client.post("/user", json=TEST_USER.dict())
    body = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert body['username'] == TEST_USER.username
    assert body['email'] == TEST_USER.email
    # delete user created during request
    op.user_delete(TEST_USER.username)


def test_user_read():
    # create logged in user
    op.user_create(TEST_USER)
    token = auth.create_access_token({'sub': TEST_USER.username})
    response = client.get("/user", headers={
        'Authorization': f'Bearer {token}',
    })
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    op.user_delete(TEST_USER.username)


def test_user_login():
    credentials = schemas.UserCredentials(
        username=TEST_USER.username,
        password=TEST_USER.password,
    )
    new_user = op.user_create(TEST_USER)
    response = client.post("/user/login", json=credentials.dict())
    assert response.status_code == status.HTTP_200_OK
    new_user.delete()


def test_game_create():
    user_new1 = op.user_create(TEST_USER)
    user_new2 = op.user_create(TEST_USER2)

    game_form = forms.GameForm(
        black=user_new1.username,
        white=user_new2.username,
        starting_formation=enums.Formation.GERMAN_DAISY.value,
    )
    response = client.post("/game", json=game_form.dict())
    body = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    user_new1.delete()
    user_new2.delete()
