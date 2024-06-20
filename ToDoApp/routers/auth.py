from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


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


# Creating dependency variable to avoid duplicate use
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth")
async def create_user(db: db_dependency, create_user_request: UserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()
