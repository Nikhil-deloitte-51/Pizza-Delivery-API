from sqlalchemy import Column, Integer, String

from database import Base

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key= True, index=True)
    name=Column(String)
    description = Column(String)
    price = Column(String)
    type = Column(String)