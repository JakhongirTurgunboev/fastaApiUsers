from sqlalchemy.orm import Session
from sqlalchemy import text
from .utils import UserCreate, UserUpdate
from . import models


def create_user(db: Session, user: UserCreate):
    # Assuming 'user.password' is already hashed, you can validate the email here.
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        return None  # User with the same email already exists, return None or handle as needed

    # If email is unique, proceed with creating the user
    sql = text(
        "INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password) RETURNING id"
    )

    result = db.execute(sql, {
        "username": user.username,
        "email": user.email,
        "hashed_password": user.password  # Assuming 'user.password' is already hashed
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
    sql = text(
        "UPDATE users SET username = :username, email = :email WHERE id = :user_id"
    )
    db.execute(sql, {"user_id": user_id, "username": user.username, "email": user.email})
    db.commit()
    result = db.execute(sql, {"user_id": user_id})
    user = result.fetchone()
    return user


def delete_user(db: Session, user_id: int):
    sql = text("DELETE FROM users WHERE id = :user_id")
    db.execute(sql, {"user_id": user_id})
    db.commit()
    return {"message": "User deleted"}


def search_user(db: Session, name: str):
    sql = text("SELECT id, username, email FROM users WHERE username = :name")
    result = db.execute(sql, {"name": name})
    users = result.fetchall()
    return users
