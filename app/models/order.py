from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    status = Column(String)
    description = Column(String)
    instruction = Column(String)
    order_number = Column(Integer)

    user = relationship("User")
    # pizza = relationship("Pizza")