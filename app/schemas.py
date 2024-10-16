from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from enums import UserRole

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    type: str

class Pizza(PizzaBase):
    id: int

    class Config:
        orm_mode = True

class PizzaCreate(PizzaBase):
    pass

class OrderBase(BaseModel):
    user_id: int
    pizza_id: int
    status: str
    total_price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int
    pizza_id: int
    quantity: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int

    class Config:
        orm_mode= True

class CartDetails(BaseModel):
    user_id: int
    items: List[Cart]

    class Config:
        orm_mode = True

# class UserRole(str, Enum):
#     customer = 'customer'
#     admin = "admin"
#     delivery = 'delivery'

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

class DeliveryBase(BaseModel):
    order_id: int
    delivery_status: str
    comment: Optional[str]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    id: int

    class Config:
        orm_mode = True

class OrderwithDeliveryDetails(Order):
    delivery_status: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[datetime]= None
    end_time: Optional[datetime]= None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None