from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json = {"email":"halo@gmail.com", "password":"password123"})
    print(response.json())
    assert response.status_code == 201
