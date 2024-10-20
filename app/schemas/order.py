from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    pizza_id: int
    status: str
    total_price: Optional[float]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class OrderwithDeliveryDetails(Order):
    delivery_status: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[datetime]= None
    end_time: Optional[datetime]= None