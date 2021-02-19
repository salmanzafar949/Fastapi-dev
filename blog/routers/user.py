from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import models
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResource, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=pwd_cxt.hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/user', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResource], tags=['User'])
def show_all(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResource, tags=['User'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(detail=f"User with {user_id} do no exist", status_code=status.HTTP_404_NOT_FOUND)

    return user
