from typing import Annotated  # Importing Annotated for type annotations with metadata
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import FastAPI, Depends, HTTPException, Path  # Importing FastAPI, Depends for dependency injection
import models  # Importing the models module containing the database models
from models import ToDos  # Importing the ToDos model from the models module
from database import engine, SessionLocal  # Importing the engine and SessionLocal for database interaction
from starlette import status  # Importing status codes from starlette
from pydantic import BaseModel, Field

# Create an instance of the FastAPI class
app = FastAPI(title="ToDo API using FastAPI by Hasan", description="ToDoApp By FastAPI", version="1.0.0")

# Create all the database tables defined in the models module
models.Base.metadata.create_all(bind=engine)


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


# Creating dependency variable to avoid duplicate use
db_dependency = Annotated[Session, Depends(get_db)]


class ToDoRequest(BaseModel):
    """
    This class defines the schema for a ToDo item request.
    It is used to validate and structure the data for creating or updating ToDo items.

    Attributes:
        title (str): The title of the ToDo item, must be between 3 and 70 characters.
        description (str): A brief description of the ToDo item, must be between 3 and 120 characters.
        priority (int): The priority level of the ToDo item, must be an integer between 1 and 5 (inclusive).
        completed (bool): A boolean indicating whether the ToDo item is completed or not.
    """

    # The title of the ToDo item
    title: str = Field(min_length=3, max_length=70, description="The title of the ToDo item (3-70 characters)")

    # A brief description of the ToDo item
    description: str = Field(min_length=3, max_length=120,
                             description="A brief description of the ToDo item (3-120 characters)")

    # The priority level of the ToDo item
    priority: int = Field(gt=0, lt=6, description="The priority level of the ToDo item (1-5)")

    # A boolean indicating whether the ToDo item is completed or not
    completed: bool


# Define a route to handle GET requests at the root URL
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    """
    Endpoint to read all ToDos from the database.
    - `db`: The database session provided by the `get_db` dependency.

    Returns a list of all ToDo items.
    """
    return db.query(ToDos).all()


# Define a route to handle GET requests to fetch a single ToDo by its ID
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_single_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Endpoint to read a single ToDo by ID.
    - `todo_id`: The ID of the ToDo item to retrieve, must be greater than 0.
    - `db`: The database session provided by the `get_db` dependency.

    If the ToDo item is found, returns the ToDo item.
    If not found, raises a 404 HTTPException with the detail "ToDo not found".
    """
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="ToDo not found")


# Define a route to handle POST requests to create a new ToDo item
@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: ToDoRequest):
    """
    Endpoint to create a new ToDo item.

    Parameters:
    - `db`: Dependency to obtain a database session.
    - `todo_request`: Request body containing details of the ToDo item to be created.

    Creates a new ToDo item instance using the data provided in `todo_request`.
    Adds the new ToDo item to the database session (`db`) and commits the transaction.
    Returns the created ToDo item.
    """
    # Create a new instance of ToDos model using data from todo_request
    todo_model = ToDos(**todo_request.dict())

    # Add the new ToDo item to the database session
    db.add(todo_model)

    # Commit the session to save the new ToDo item in the database
    db.commit()

    # Return the created ToDo item
    return todo_model






# https://gale.udemy.com/course/fastapi-the-complete-course/learn/lecture/29025864#overview
