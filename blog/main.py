from fastapi import FastAPI, Depends, status, Response, HTTPException
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


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def store(blog: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=blog.title, body=blog.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)

    return newBlog


@app.get('/blogs', status_code=status.HTTP_200_OK)
def blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
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
def update(id, blog:schemas.Blog, db:Session=Depends(get_db)):
    updateBlog = db.query(models.Blog).filter(models.Blog.id == id)

    if not updateBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Blog Found')
    else:
        updateBlog.update(blog, synchronize_session=True)
        db.commit()
        return {
            "data": "success",
            'blog': updateBlog.first()
        }

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {}