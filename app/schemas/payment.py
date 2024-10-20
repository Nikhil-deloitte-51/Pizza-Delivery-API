from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    payment_method: str
    created_at: Optional[datetime]= None

class Payment(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str