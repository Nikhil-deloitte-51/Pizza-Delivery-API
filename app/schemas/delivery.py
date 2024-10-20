from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from enums import DeliveryStatus

class DeliveryBase(BaseModel):
    order_id: int
    delivery_status: DeliveryStatus
    comment: Optional[str]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    id: int

    class Config:
        orm_mode = True

class DeliveryRequest(BaseModel):
    user_id: int
    order_number: str
    delivery_address: str

class DeliveryStatusUpdate(BaseModel):
    delivery_id: int
    delivery_status: DeliveryStatus
    comment: Optional[str] = None