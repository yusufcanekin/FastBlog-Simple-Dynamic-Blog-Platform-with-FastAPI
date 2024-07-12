import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import schemas
import pytest
import jwt
from app.config import settings
from database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email":"hello@gmail.com", "password":"password123"}
    response = client.post("/users/", json=user_data)
    user = response.json()
    user["password"] = user_data["password"]
    return user


def test_create_user(client):
    response = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})
    user = schemas.UserResponse(**response.json())
    assert user.email == "hello123@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login/", data={"username": test_user["email"], "password":test_user["password"]})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id: str = payload.get("user_id")
    assert response.status_code == 200
    assert test_user["id"] == id
    assert login_res.token_type == "bearer"

def test_incorrect_login(client, test_user):
    response = client.post("/login/", data={"username": test_user["email"], "password":"wrong"})
    assert response.status_code == 403 or response.status_code == 422

