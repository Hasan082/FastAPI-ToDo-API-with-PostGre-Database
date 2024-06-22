# FastAPI ToDo API

This project implements a RESTful API for managing ToDo items using FastAPI, SQLAlchemy for database interaction, and Pydantic for data validation. It includes authentication, user management, and CRUD operations for ToDo items.

## Setup

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

4. The API will be available at `http://localhost:8000`. OpenAPI documentation is available at `http://localhost:8000/docs`.

### Environment

- Python 3.9 or higher
- SQLite (default for development, can be changed in `database.py`)

## Project Structure

```
.
├── main.py                 # Main FastAPI application
├── database.py             # Database setup and SessionLocal definition
├── models.py               # SQLAlchemy models (User, ToDos)
├── auth.py                 # Authentication and token handling
├── routers/
│   ├── auth.py             # Authentication router
│   ├── todos.py            # ToDo operations router
│   ├── admin.py            # Admin routes (for admin-only operations)
│   └── users.py            # User routes (user profile and password management)
├── README.md               # This README file
└── requirements.txt        # Project dependencies
```

## Files Description

### `main.py`

This is the main entry point of the FastAPI application. It sets up the FastAPI application instance (`app`), creates database tables from models, and includes routers for different parts of the API (auth, todos, admin, users).

### `database.py`

Contains the database configuration using SQLAlchemy. Defines `SessionLocal` for creating database sessions and initializes the SQLite database.

### `models.py`

Defines SQLAlchemy models:
- `User`: Represents user details including username, email, hashed password, etc.
- `ToDos`: Represents ToDo items with title, description, priority, completion status, and owner relationship.

### `auth.py`

Handles authentication and token generation using JWT (JSON Web Tokens). Includes functions for password hashing, token verification, and current user retrieval.

### `routers/`

Contains routers for different parts of the API:
- `auth.py`: Routes for authentication (login, token generation)
- `todos.py`: CRUD operations for ToDo items (create, read, update, delete)
- `admin.py`: Admin-only routes (fetch all todos, delete todo by ID)
- `users.py`: Routes for user profile (fetch current user details, update password)

### `README.md`

This file provides an overview of the project, setup instructions, and a description of each file's purpose and contents.

### `requirements.txt`

Lists all Python dependencies required for the project. Install using `pip install -r requirements.txt`.

## Usage

- **Authentication**: Use `/auth/token` endpoint to obtain JWT token. Include `Bearer <token>` in headers for authenticated routes.
- **ToDo Operations**: Use CRUD operations (`GET`, `POST`, `PUT`, `DELETE`) on `/todos` endpoint.
- **User Profile**: Update password using `/users/me/password` endpoint. Fetch user details with `/users/me`.

## Notes

- Ensure Python 3.9 or higher and SQLite are installed.
- Adjust database configuration (`database.py`) for production environments.
- Securely manage `SECRET_KEY` and environment variables in production.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [Starlette Documentation](https://www.starlette.io/)

