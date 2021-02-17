from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get('/')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {
            'data': f'{limit} published blogs'
        }
    else:
        return {
            'data': f'{limit} from the blog List'
        }


@app.get('/blog/unpublished')
def unpublished_blogs():
    return {
        'data': 'unpublished blogs'
    }


@app.get('/blog/{id}')
def show(id: int):
    return {
        'data': id
    }


@app.post('/blog')
def store(blog: Blog):
    return blog
