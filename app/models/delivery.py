from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    delivery_status = Column(String)
    comment = Column(String, nullable= True)
    start_time = Column(DateTime, nullable= True)
    end_time = Column(DateTime, nullable= True)
    delivery_address = Column(String)
    order_number = Column(String)

    user = relationship("User")