from fastapi import FastAPI, Depends
from . import schemas
from . import models
from .database import engine, SessionDb
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionDb()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def store(blog: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=blog.title, body=blog.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)

    return newBlog


@app.get('/blogs')
def blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{id}')
def show(id, db:Session=Depends(get_db)):
    return db.query(models.Blog).filter(models.Blog.id == id).first()