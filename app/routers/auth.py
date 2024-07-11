from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas, utils, models, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post('/', response_model=schemas.Token)
# When you make user_credentials a dependency, it will store the credentials
# as username and password. You also should send data from Postman as form-data, instead of raw body.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    
    #CREATıNG TOKEN

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}
    

