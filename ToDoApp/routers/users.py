from typing import Annotated  # Importing Annotated for type annotations with metadata
from passlib.context import CryptContext
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import APIRouter, Depends, HTTPException, Path  # Importing FastAPI, Depends for dependency injection
from models import ToDos, User  # Importing the ToDos model from the models module
from database import SessionLocal  # Importing the engine and SessionLocal for database interaction
from starlette import status  # Importing status codes from starlette
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


# Dependency function to get a database session
def get_db():
    """
    Dependency function that provides a database session.
    The session is yielded to the endpoint and closed automatically after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    password: str
    new_password: str


# Creating dependency variable to avoid duplicate use
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(User).filter(User.id == user.get('user_id')).first()


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, userVerification: UserVerification):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_model = db.query(User).filter(User.id == user.get('user_id')).first()

    if not bcrypt_context.verify(userVerification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    user_model.hashed_password = bcrypt_context.hash(userVerification.new_password)

    db.add(user_model)
    db.commit()
