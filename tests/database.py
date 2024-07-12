import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import SessionLocal, get_db
from app import models
import pytest
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:mypassword@0.0.0.0:5431/mydatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
       
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)