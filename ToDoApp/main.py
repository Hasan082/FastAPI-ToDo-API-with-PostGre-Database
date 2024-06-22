# Importing FastAPI class from the FastAPI library to create the application instance
from fastapi import FastAPI

# Importing the models module, which contains the database models (ORM classes)
import models

# Importing the database engine, which is used to connect to the database and execute SQL commands
from database import engine

# Importing the routers for different modules of the application: auth, todos, admin, and users
from routers import auth, todos, admin, users

# Create an instance of the FastAPI class
# The instance 'app' represents the web application itself
app = FastAPI(
    title="ToDo API using FastAPI by Hasan",  # Title of the API for documentation
    description="ToDoApp By FastAPI",        # Description of the API for documentation
    version="1.0.0"                          # Version of the API
)

# Create all the database tables defined in the models module
# This line ensures that all tables defined in the ORM models are created in the database
models.Base.metadata.create_all(bind=engine)

# Include the auth router, which handles authentication-related endpoints
# This router is defined in the routers/auth.py module
app.include_router(auth.router)

# Include the todos router, which handles CRUD operations for ToDo items
# This router is defined in the routers/todos.py module
app.include_router(todos.router)

# Include the admin router, which handles admin-related endpoints
# This router is defined in the routers/admin.py module
app.include_router(admin.router)

# Include the users router, which handles user-related endpoints
# This router is defined in the routers/users.py module
app.include_router(users.router)

# The application is now configured with the necessary routers and is ready to handle requests

