from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from schemas import User
from database import get_db
from sqlalchemy.orm import Session
import utils, schemas, models

router = APIRouter()


@router.post("/create_user", status_code = status.HTTP_201_CREATED,response_model=schemas.userResponse)
def create_user(user : User, db : Session = Depends(get_db)):
    #hasghing the password
    hash_passwd = utils.hash(user.password)
    user.password = hash_passwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get_user/{id}")
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} not found!")
    return user

@router.get("/getUsers")
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts