from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
