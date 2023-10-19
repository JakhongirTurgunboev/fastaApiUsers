from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
import os
from database import crud, models, database, utils
from database.database import get_db
from api import auth

app = FastAPI()

# Configure the log directory and file name
log_dir = "logs"  # Name of the directory to store log files
log_file = "app.log"  # Name of the log file

# Create the logs directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, log_file)),
        logging.StreamHandler(),
    ]
)

# OAuth2 for JWT Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Check if the "users" table exists and create it if not
database.create_users_table_if_not_exists()


# CRUD Operations for Users
# Create a User
@app.post("/users/", response_model=utils.UserResponse)
async def create_user(user: utils.UserCreate, db: Session = Depends(get_db)):
    user_id = crud.create_user(db, user)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User with the same email already exists or invalid email/password")
    created_user = models.User(username=user.username,
                               email=user.email,
                               hashed_password=user.password,
                               id=user_id)
    db.commit()

    return created_user


# Get User by ID
@app.get("/users/{user_id}", response_model=utils.UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Get All Users
@app.get("/users/", response_model=List[utils.UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


# Update User by ID
@app.put("/users/{user_id}", response_model=utils.UserResponse)
async def update_user(user_id: int, user: utils.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# Delete User by ID
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


# Search for a User by Name
@app.get("/users/search/", response_model=List[utils.UserResponse])
async def search_user(name: str, db: Session = Depends(get_db)):
    users = crud.search_user(db, name)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


# Token based authentication
@app.post("/token", response_model=utils.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)  # Implement your authentication logic
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    expires = timedelta(minutes=30)  # Token expires in 30 minutes
    return auth.create_access_token(data={"sub": user.username}, expires_delta=expires)


