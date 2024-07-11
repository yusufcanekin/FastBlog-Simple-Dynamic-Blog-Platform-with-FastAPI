import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import models, schemas, utils, oauth2
from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**dict(user)) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found.")
    return user

