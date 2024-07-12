from app import schemas
import pytest
def test_get_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    print(response.json())
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unaouthorized_get_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unaouthorized_get_post(client, test_posts):
    for post in test_posts:
        response = client.get(f"/posts/{post.id}")
        assert response.status_code == 401

def test_get_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/213423")
    assert response.status_code == 404

def test_get_post(authorized_client, test_posts):
    for post in test_posts:
        response = authorized_client.get(f"/posts/{post.id}")
        assert response.status_code == 200
        assert response.json()["id"] == post.id
        assert response.json()["content"] == post.content

@pytest.mark.parametrize("title, content", [
    ("title1", "content1"),
    ("title2", "content2")
])
def test_create_post(authorized_client, title, content):
    response = authorized_client.post("/posts/", json={"title" :title, "content":content})
    assert response.status_code == 201

@pytest.mark.parametrize("title, content", [
    ("title1", "content1"),
    ("title2", "content2")
])
def test_unauthorized_create_post(client, title, content):
    response = client.post("/posts/", json={"title" :title, "content":content})
    assert response.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts, session):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_unauthorized_delete_post(client, test_user, session, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_nonexistent_delete_post(authorized_client):
    response = authorized_client.delete(f"/posts/2341543")
    assert response.status_code == 404


def test_update_post(authorized_client, test_posts):
    data = {
    "title":"updated title",
    "content": "updated content"
}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    assert response.status_code == 200




