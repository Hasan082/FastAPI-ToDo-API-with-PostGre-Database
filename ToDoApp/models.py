# Importing necessary components from SQLAlchemy and database module
from database import Base  # Importing the Base class from the database module for declarative base class
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Importing column types and ForeignKey
from sqlalchemy.orm import relationship  # Importing relationship for setting up ORM relationships


# Define the User model, inheriting from Base
class User(Base):
    __tablename__ = 'users'  # Specifies the name of the database table for this model

    # Defining columns in the 'users' table
    id = Column(Integer, primary_key=True, index=True)  # Primary key column, indexed for faster lookups
    email = Column(String, unique=True)  # Email column, must be unique
    username = Column(String, unique=True)  # Username column, must be unique
    first_name = Column(String)  # First name column
    last_name = Column(String)  # Last name column
    hashed_password = Column(String)  # Hashed password column for storing encrypted passwords
    is_active = Column(Boolean, default=True)  # Boolean column to indicate if the user is active, default is True
    role = Column(String)  # Role column to store user roles


    # Setting up a one-to-many relationship with the ToDos model The 'todos' attribute will contain a list of ToDos
    # objects associated with this User back_populates='owner' indicates that the 'owner' relationship in the ToDos
    # model will be used to handle the reverse relationship
    todos = relationship('ToDos', back_populates='owner')


# Define the ToDos model, inheriting from Base
class ToDos(Base):
    __tablename__ = 'todos'  # Specifies the name of the database table for this model

    # Defining columns in the 'todos' table
    id = Column(Integer, primary_key=True, index=True)  # Primary key column, indexed for faster lookups
    title = Column(String)  # Title column for the ToDo item
    description = Column(String)  # Description column for the ToDo item
    priority = Column(Integer)  # Priority column for the ToDo item, expects an integer value
    completed = Column(Boolean, default=False)  # Boolean column to indicate if the ToDo is completed, default is False
    owner_id = Column(Integer, ForeignKey('users.id'),
                      nullable=False)  # Foreign key column referencing 'id' in the 'users' table, cannot be null

    # Setting up a many-to-one relationship with the User model The 'owner' attribute will contain the User object
    # associated with this ToDo back_populates='todos' indicates that the 'todos' relationship in the User model will
    #  be used to handle the reverse relationship
    owner = relationship('User', back_populates='todos')
