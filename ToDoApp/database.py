# Importing necessary components from SQLAlchemy
from sqlalchemy import create_engine  # Used to create a connection to the database
from sqlalchemy.orm import sessionmaker  # Used to create a configured "Session" class
from sqlalchemy.ext.declarative import declarative_base  # Used to create a base class for our ORM models

# Defining the database URL
# Here, we are using SQLite as the database and specifying the database file as 'todosapp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost:5432/Todoappdatabase'

# Creating the SQLAlchemy engine
# The engine object is how SQLAlchemy communicates with the database
# 'check_same_thread': False is specific to SQLite and allows the use of the same connection across multiple threads
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating a configured "Session" class sessionmaker is a factory for creating new Session objects autocommit=False:
# Transactions are managed manually, meaning we need to explicitly commit or rollback transactions autoflush=False:
# Changes to the database are not immediately flushed to the database; this happens only when explicitly committed
# bind=engine: The session is bound to the engine, meaning it will use this engine to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a base class for our ORM models
# All ORM models will inherit from this base class
# This base class includes the necessary metadata and methods to map classes to database tables
Base = declarative_base()



