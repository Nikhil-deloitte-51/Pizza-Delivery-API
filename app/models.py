from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import List, Optional
from database import Base
from passlib.context import CryptContext
from enum import Enum as PyEnum

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

Base = declarative_base()

class UserRole(PyEnum):
    customer = 'customer'
    admin = 'admin'
    delivery = 'delivery'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index = True)
    username = Column(String, unique=True, index= True)
    password = Column(String)
    email = Column(String)
    # role = Column(Enum(UserRole))
    role = Column(String)

    def hash_password(password:str):
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password:str):
        return pwd_context.verify(plain_password, hashed_password)

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key= True, index=True)
    name=Column(String)
    description = Column(String)
    price = Column(String)
    type = Column(String)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    status = Column(String)
    total_price = Column(Float)
    user = relationship("User")
    pizza = relationship("Pizza")

class CartResponse(BaseModel):
   id: int
   user_id: int
   items: List
   
   class Config:
    orm_mode = True

class CartItemCreate(BaseModel):
    pizza_id: int
    quantity: int = Field(default = 1, ge=1)

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    quantity = Column(Integer, default=1)

    user = relationship("User")
    pizza = relationship("Pizza")

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key= True, index= True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    delivery_status = Column(String)
    comment = Column(String, nullable= True)
    start_time = Column(DateTime, nullable= True)
    end_time = Column(DateTime, nullable= True)

    order = relationship("Order")