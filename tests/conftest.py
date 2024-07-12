'''
This file is seen by the all files in the same package, no need to import fixtures.
'''

import pytest
from database import client, session
from app.oauth2 import create_access_token
from app import models

@pytest.fixture
def test_user(client):
    user_data = {"email":"hello@gmail.com", "password":"password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    user["password"] = user_data["password"]
    return user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id'] 
    }, ]

    def converter(post):
        return models.Post(**post)
    post_list = list(map(converter, posts_data))

    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
