from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
import databases

# Define the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SQLAlchemy session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a databases Database instance for use with async database operations
database = databases.Database(SQLALCHEMY_DATABASE_URL)

# Define the Base class for declarative models
Base = declarative_base()


def create_users_table_if_not_exists():
    # Attempt to create the "users" table
    try:
        from .models import User  # Import the User model where "users" table is defined
        Base.metadata.create_all(bind=engine, tables=[User.__table__])
    except ProgrammingError:
        # Table already exists, no need to create it again
        pass


# Dependency to get the database session (used in API routes)
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
