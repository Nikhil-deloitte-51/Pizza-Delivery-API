from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    quantity = Column(Integer, default=1)
    total = Column(Integer)

    user = relationship("User")
    pizza = relationship("Pizza")