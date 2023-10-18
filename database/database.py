from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.orm import Session

# Define the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SQLAlchemy session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Pydantic model base class for database models
Base = declarative_base()

# Create a databases Database instance for use with async database operations
database = Database(SQLALCHEMY_DATABASE_URL)


# Dependency to get the database session (used in API routes)
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
