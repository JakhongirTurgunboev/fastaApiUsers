import re

import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import text
from .utils import UserCreate, UserUpdate
from . import models


def create_user(db: Session, user: UserCreate):
    # Validate the email with a regular expression
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user.email):
        return None  # Invalid email format, return None or handle as needed

    # Validate the password
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", user.password):
        return None  # Password does not meet the criteria, return None or handle as needed

    # Check if a user with the same email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        return None  # User with the same email already exists, return None or handle as needed

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # If email is unique and password is valid, proceed with creating the user
    sql = text(
        "INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password) RETURNING id"
    )

    result = db.execute(sql, {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password.decode('utf-8')  # Convert bytes to a string
    })

    user_id = result.scalar()
    return user_id


def get_user(db: Session, user_id: int):
    sql = text("SELECT id, username, email FROM users WHERE id = :user_id")
    result = db.execute(sql, {"user_id": user_id})
    user = result.fetchone()
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    sql = text("SELECT id, username, email FROM users LIMIT :limit OFFSET :offset")
    result = db.execute(sql, {"offset": skip, "limit": limit})
    users = result.fetchall()
    return users


def update_user(db: Session, user_id: int, user: UserUpdate):
    # Retrieve the user to update
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()

    if existing_user:
        # Validate the email with a regular expression
        if user.email and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user.email):
            return None  # Invalid email format, return None or handle as needed

        # Update the user's attributes
        if user.username:
            existing_user.username = user.username
        if user.email:
            existing_user.email = user.email

        # Commit the changes to the database
        db.commit()

        # Return the updated user
        updated_user = {
            "id": existing_user.id,
            "username": existing_user.username,
            "email": existing_user.email
        }

        return updated_user

    return None  # User not found


def delete_user(db: Session, user_id: int):
    sql = text("DELETE FROM users WHERE id = :user_id")
    db.execute(sql, {"user_id": user_id})
    db.commit()
    return {"message": "User deleted"}


def search_user(db: Session, name: str):
    # Use a SQL query with a wildcard '%' to search for usernames containing 'name'
    sql = text("SELECT id, username, email FROM users WHERE username LIKE :name")
    result = db.execute(sql, {"name": f"%{name}%"})
    users = result.fetchall()
    return users
