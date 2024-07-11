import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from app import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # should be the same as the path of login function at auth.py

SECRET_KEY = settings.secret_key
ALGORİTHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: schemas.TokenData):
    to_encode = data.copy()


    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORİTHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORİTHM)
        print(payload)
        id: str = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError: 
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials")
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user