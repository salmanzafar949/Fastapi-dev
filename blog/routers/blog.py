from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import blog as blogRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.BlogResource)
def store(blog: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepo.save_all(blog, db)


@router.get('', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogResource])
def blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogRepo.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.BlogResource)
def show(id: int, db: Session = Depends(get_db)):
    return blogRepo.show(id, db)


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepo.update(id, blog, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return blogRepo.destroy(id, db)
