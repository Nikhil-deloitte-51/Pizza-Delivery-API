from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from enums import UserRole

class UserBase(BaseModel):
    username: str = Field(..., example='nikhil')
    email: EmailStr = Field(..., example="nk@gmail.com")
    role: UserRole = Field(..., example = "customer")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example='strongpassword')

class UserRespone(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None