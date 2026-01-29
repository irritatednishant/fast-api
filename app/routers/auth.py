from fastapi import FastAPI, HTTPException, Depends, Response, APIRouter, status
from argon2.exceptions import VerifyMismatchError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLoging
import utils, oauth2
router = APIRouter(
    tags=["Authentication"]
    )

@router.post('/login')
def user_login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Credentials!")
    try:
        utils.verify(user.password,user_credentials.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Credentials!")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id} )

    return {"access_token" : access_token ,"token_type" : "bearer"}