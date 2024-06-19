from typing import Annotated  # Importing Annotated for type annotations with metadata
from sqlalchemy.orm import Session  # Importing Session for type hinting
from fastapi import FastAPI, Depends, HTTPException  # Importing FastAPIand, Depends for dependency injection
import models  # Importing the models module containing the database models
from models import ToDos  # Importing the ToDos model from the models module
from database import engine, SessionLocal  # Importing the engine and SessionLocal for database interaction

# Create an instance of the FastAPI class
app = FastAPI(title="ToDo API using FirstAPI by Hasan", description="ToDoApp By FirstAPI", version="1.0.0")

# Create all the database tables defined in the models module
models.Base.metadata.create_all(bind=engine)


# Dependency function to get a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to be used in the endpoint
        yield db
    finally:
        # Close the session when the request is finished
        db.close()


# Creating dependency variable avoiding duplicate use
db_dependency = Annotated[Session, Depends(get_db)]


# Define a route to handle GET requests at the root URL
@app.get("/")
async def read_all(db: db_dependency):
    """
    Endpoint to read all ToDos from the database.
    - `db`: The db session provided by the `get_db` dependency.
    """
    # Query the ToDos table and return all records
    return db.query(ToDos).all()


# Define a route to handle GET requests to fetch a single ToDo by its ID
@app.get("/todo/{todo_id}")
async def read_single_todo(todo_id: int, db: db_dependency):
    """
    Endpoint to read a single ToDo by ID.
    - `todo_id`: The ID of the ToDo item to retrieve.
    - `db`: The database session provided by the `get_db` dependency.
    """
    # Query the ToDos table for the ToDo with the specified ID
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    # If the ToDo item is found, return it
    if todo_model is not None:
        return todo_model

    # If the ToDo item is not found, raise a 404 HTTPException
    raise HTTPException(status_code=404, detail="ToDo not found")







# https://gale.udemy.com/course/fastapi-the-complete-course/learn/lecture/29025864#overview
