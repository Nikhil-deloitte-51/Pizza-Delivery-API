from sqlalchemy import Integer, Column, String
from passlib.context import CryptContext

from database import Base

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

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