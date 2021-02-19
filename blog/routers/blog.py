from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from .. import schemas
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.BlogResource, tags=['Blog'])
def store(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogResource], tags=['Blog'])
def blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.BlogResource, tags=['Blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model Not Found')
        # return {
        #     'detail': 'Blog Not Found'
        # }

    return blog


@router.put('/blog/{id}', status_code=status.HTTP_200_OK, tags=['Blog'])
def update(id, blog: schemas.Blog, db: Session = Depends(get_db)):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not updated_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Blog Found')
    else:
        updated_blog.update(blog)
        db.commit()
        return {
            "data": "success",
            'blog': updated_blog.first()
        }


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {}
