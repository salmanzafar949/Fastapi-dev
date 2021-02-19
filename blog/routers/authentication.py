from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import _token
from fastapi.security import OAuth2PasswordRequestForm
ctx = CryptContext(schemes=['bcrypt'], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if not ctx.verify(request.password, user.password):
        raise HTTPException(detail="Invalid Credentials", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    access_token = _token.create_access_token(data={'sub': user.email})

    return {
        'access_token': access_token
    }