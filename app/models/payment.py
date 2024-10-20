from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from database import Base
from sqlalchemy.orm import relationship

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    payment_method = Column(String)
    created_at = Column(DateTime)

    order = relationship("Order")