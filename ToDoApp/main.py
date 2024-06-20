from fastapi import FastAPI # Importing FastAPI, Depends for dependency injection
import models  # Importing the models module containing the database models
from database import engine # Importing the engine and SessionLocal for database interaction
from routers import auth, todos


# Create an instance of the FastAPI class
app = FastAPI(title="ToDo API using FastAPI by Hasan", description="ToDoApp By FastAPI", version="1.0.0")

# Create all the database tables defined in the models module
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
