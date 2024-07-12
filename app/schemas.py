from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr #imported from pydantic, checks whether it is a valid e-mail
    class Config(ConfigDict):
        orm_mode = True

class UserCreate(UserBase):
    password:str
    class Config(ConfigDict):
        orm_mode = True

class UserResponse(UserBase):
    id:int
    created_at:datetime
    class Config(ConfigDict):
        orm_mode = True

class User(UserResponse):
    password:str
    class Config(ConfigDict):
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    class Config(ConfigDict):
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str = None
    class Config(ConfigDict):
        orm_mode = True

class Post(PostBase):
    id:int
    created_at: datetime
    user_id:int
    owner : UserResponse
    class Config(ConfigDict):
        orm_mode = True
    
class PostCreate(PostBase):
    class Config(ConfigDict):
        orm_mode = True
    pass

class UserBase(BaseModel):
    email:EmailStr #imported from pydantic, checks whether it is a valid e-mail
    class Config(ConfigDict):
        orm_mode = True

class UserCreate(UserBase):
    password:str
    class Config(ConfigDict):
        orm_mode = True

class UserResponse(UserBase):
    id:int
    created_at:datetime
    class Config(ConfigDict):
        orm_mode = True

class User(UserResponse):
    password:str
    class Config(ConfigDict):
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    class Config(ConfigDict):
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str
    class Config(ConfigDict):
        orm_mode = True

class TokenData(BaseModel):
    id:int
    class Config(ConfigDict):
        orm_mode = True