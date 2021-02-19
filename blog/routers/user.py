from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import userrepository

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResource)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return userrepository.store(request, db)


@router.get('', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResource])
def show_all(db: Session = Depends(get_db)):
    return userrepository.get_all(db)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResource)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return userrepository.show(user_id, db)
