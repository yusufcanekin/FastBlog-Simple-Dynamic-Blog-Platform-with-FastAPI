import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.config import settings

database_hostname = settings.database_hostname
database_port = settings.database_port
database_password = settings.database_password
database_name = settings.database_name
database_username = settings.database_username

SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
       
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
