from fastapi import status
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_created_user_valid():
    test_user = {
        'username': 'peterpopper',
        'email': 'peter@popper.com',
        'password': 'password',
    }
    response = client.post("/user", json=test_user)
    body = response.json()
    print(body)
    assert response.status_code == status.HTTP_201_CREATED
    assert body['username'] <= test_user['username']
    assert body['email'] <= test_user['email']
