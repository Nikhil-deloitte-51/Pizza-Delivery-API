from pydantic import BaseModel
from typing import List

class CartBase(BaseModel):
    # user_id: int
    pizza_id: int
    quantity: int
    total: int

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

class CheckoutRequest(BaseModel):
    pizza_id: int
    quantity: int
    total: int
