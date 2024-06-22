from typing import Annotated  # Importing Annotated for type annotations with metadata
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import APIRouter, Depends, HTTPException, Path  # Importing FastAPI, Depends for dependency injection
from models import ToDos  # Importing the ToDos model from the models module
from database import SessionLocal  # Importing the engine and SessionLocal for database interaction
from starlette import status  # Importing status codes from starlette
from pydantic import BaseModel, Field
from .auth import get_current_user  # Importing the get_current_user function from auth module

# Creating an API router for admin-specific routes with a prefix and tags
router = APIRouter(
    prefix='/admin',
    tags=['admin']
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


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    """
    Endpoint to read all ToDos for admin users.

    Parameters:
    - `user`: The current authenticated user with admin privileges.
    - `db`: Dependency to obtain a database session.

    Returns a list of all ToDo items if the user is authenticated and has admin privileges.
    Raises a 401 HTTPException if the user is not authenticated or is not an admin.
    """
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    return db.query(ToDos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Endpoint to delete a specific ToDo item by its ID for admin users.

    Parameters:
    - `user`: The current authenticated user with admin privileges.
    - `db`: Dependency to obtain a database session.
    - `todo_id`: Path parameter representing the ID of the ToDo item to delete, must be greater than 0.

    Deletes the ToDo item identified by `todo_id` if the user is authenticated and has admin privileges.
    Raises a 401 HTTPException if the user is not authenticated or is not an admin.
    Raises a 404 HTTPException if the ToDo item is not found.
    """
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')

    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ToDo not found')

    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()
