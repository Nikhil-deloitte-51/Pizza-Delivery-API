from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

# from routers.user import get_current_user

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models.user import User
from enums import UserRole
from schemas.user import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def create_access_token(data: dict, 
                        expires_delta: timedelta = None
                        ):
    """Create a JWT token with an expiration time."""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow()+ timedelta(minutes = 15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), 
                     token: str= Depends(oauth2_scheme)
                     ):
    """Get the current user's information using the provided JWT token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"www-authenticate": "Bearer"},
    )
    try:
        # Decode the token and retrieve username 
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.username==token_data.username
        ).first()
    
    if user is None:
        raise credentials_exception

    return user

def role_required(required_role: UserRole):
    def role_checker(current_user:User = Depends(get_current_user)):
        print(f"current user role: {current_user.role}, Required role: {required_role}")
        if current_user.role!= required_role:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Operation not permitted",
                headers = {"WWW-Authenticate": "Bearer"},
            )
        return current_user
    return role_checker