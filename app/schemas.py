from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr #imported from pydantic, checks whether it is a valid e-mail

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id:int
    created_at:datetime

class User(UserResponse):
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title: str
    content: str = None,

class Post(PostBase):
    id:int
    created_at: datetime
    user_id:int
    owner : UserResponse
    
class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    email:EmailStr #imported from pydantic, checks whether it is a valid e-mail

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id:int
    created_at:datetime

class User(UserResponse):
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int