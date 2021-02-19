from pydantic import BaseModel
from typing import Optional, List


class BlogBase(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserResource(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class BlogResource(BaseModel):
    title: str
    body: str
    author: UserResource

    class Config:
        orm_mode = True
