from typing import Annotated  # Importing Annotated for type annotations with metadata
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import FastAPI, Depends, HTTPException, Path  # Importing FastAPI, Depends for dependency injection
import models  # Importing the models module containing the database models
from models import ToDos  # Importing the ToDos model from the models module
from database import engine, SessionLocal  # Importing the engine and SessionLocal for database interaction
from starlette import status  # Importing status codes from starlette

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

# https://gale.udemy.com/course/fastapi-the-complete-course/learn/lecture/29025864#overview
