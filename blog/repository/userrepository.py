from fastapi import HTTPException, status
from .. import schemas, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def store(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=pwd_cxt.hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all(db: Session):
    return db.query(models.User).all()


def show(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(detail=f"User with {user_id} do no exist", status_code=status.HTTP_404_NOT_FOUND)

    return user
