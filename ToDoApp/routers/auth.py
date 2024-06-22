from datetime import timedelta, datetime  # Importing necessary datetime functions
from typing import Annotated  # Importing Annotated for type annotations with metadata
from fastapi import APIRouter, Depends, HTTPException  # Importing FastAPI components for routing and dependency injection
from pydantic import BaseModel  # Importing BaseModel from Pydantic for request and response schemas
from sqlalchemy.orm import Session  # Importing Session for database operations
from starlette import status  # Importing HTTP status codes from starlette
from database import SessionLocal  # Importing SessionLocal for database session
from models import User  # Importing User model
from passlib.context import CryptContext  # Importing CryptContext for password hashing
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer  # Importing OAuth2 components for security
from jose import jwt, JWTError  # Importing JWT components from jose for token handling

# Creating an APIRouter instance for the authentication routes
router = APIRouter(
    prefix='/auth',  # Prefix for all routes in this router
    tags=['auth']  # Tag for grouping routes in the OpenAPI documentation
)

# Constants for JWT token generation
SECRET_KEY = "d46c0355cd2ebe050dff966842bf952390be478ed52e04e40cd8543ad7a6eb61"  # Secret key for signing JWT tokens
ALGORITHM = "HS256"  # Algorithm for JWT token encoding

# Initializing CryptContext for password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Initializing OAuth2PasswordBearer for token authentication
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# Pydantic model for user registration request
class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str


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


# Function to authenticate user by username and password
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


# Function to create JWT access token
def create_access_token(username: str, user_id: int, role: str, expire_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.utcnow() + expire_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependency function to get current user from the token
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or ID not found")
        return {'username': username, 'user_id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or ID not found")


# Endpoint to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED)
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


# Endpoint to generate access token on user login
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or ID not found")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}
