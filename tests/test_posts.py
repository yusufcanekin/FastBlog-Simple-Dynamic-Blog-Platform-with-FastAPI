from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:mypassword@test_db:5433/test_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
       
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

Base = declarative_base()

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json = {"email":"halo@gmail.com", "password":"password123"})
    print(response.json())
    assert response.status_code == 201
