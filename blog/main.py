from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .database import engine, SessionDb
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionDb()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def store(blog: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=blog.title, body=blog.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)

    return newBlog


@app.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.BlogResource])
def blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.BlogResource)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model Not Found')
        # return {
        #     'detail': 'Blog Not Found'
        # }

    return blog


@app.put('/blog/{id}', status_code=status.HTTP_200_OK)
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


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {}


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResource)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=pwd_cxt.hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResource])
def show_all(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResource)
def get_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(detail=f"User with {user_id} do no exist", status_code=status.HTTP_404_NOT_FOUND)

    return user
