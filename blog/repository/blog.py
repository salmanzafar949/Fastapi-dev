from sqlalchemy.orm import Session
from .. import models
from fastapi import HTTPException, status
from ..schemas import Blog


def get_all(db: Session):
    return db.query(models.Blog).all()


def save_all(request: Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model Not Found')
    return blog


def update(id: int, blog: Blog, db: Session):
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


def destroy(id: int, db: Session):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {}