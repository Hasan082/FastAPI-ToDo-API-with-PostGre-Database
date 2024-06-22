from typing import Annotated  # Importing Annotated for type annotations with metadata
from passlib.context import CryptContext
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import APIRouter, Depends, HTTPException, Path  # Importing FastAPI, Depends for dependency injection
from models import ToDos, User  # Importing the ToDos and User models from the models module
from database import SessionLocal  # Importing the engine and SessionLocal for database interaction
from starlette import status  # Importing status codes from starlette
from pydantic import BaseModel, Field
from .auth import get_current_user  # Importing the get_current_user function from auth module

# Creating an API router for user-specific routes with a prefix and tags
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


# Creating dependency variables to avoid duplicate use
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic model for password verification and update
class UserVerification(BaseModel):
    """
    Pydantic model for verifying and updating user password.

    Attributes:
        password (str): The current user password.
        new_password (str): The new password to be set.
    """
    password: str
    new_password: str


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    """
    Endpoint to fetch details of the currently authenticated user.

    Parameters:
    - `user`: The current authenticated user obtained from the request dependency.
    - `db`: Dependency to obtain a database session.

    Returns:
    - Returns the details of the current user if authenticated.
    - Raises HTTP 401 Unauthorized if the user is not authenticated.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(User).filter(User.id == user.get('user_id')).first()


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, userVerification: UserVerification):
    """
    Endpoint to update the password of the currently authenticated user.

    Parameters:
    - `user`: The current authenticated user obtained from the request dependency.
    - `db`: Dependency to obtain a database session.
    - `userVerification`: Request body containing the current password and new password.

    Updates the password of the authenticated user if the current password matches.
    Raises HTTP 401 Unauthorized if the user is not authenticated or the current password is incorrect.

    Notes:
    - Passwords are hashed using bcrypt for security.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_model = db.query(User).filter(User.id == user.get('user_id')).first()

    if not bcrypt_context.verify(userVerification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # Hash the new password before updating
    user_model.hashed_password = bcrypt_context.hash(userVerification.new_password)

    # Add the updated user model to the database session and commit the transaction
    db.add(user_model)
    db.commit()
