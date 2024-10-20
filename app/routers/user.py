from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

from models.user import User
from schemas.user import UserCreate, UserRespone, Token, TokenData
from database import get_db
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import create_access_token

router = APIRouter()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# Create user
@router.post("/users", 
             response_model= UserRespone
             )
def create_user(user: UserCreate, 
                db: Session = Depends(get_db)
                ):
    """Create a new user in the database."""

    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
        ).first()
    
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail = "Username already exists",
            )

    # Create a new user instance with hashed password
    new_user = User(
        username=user.username, 
        password=User.hash_password(user.password), # Hash the password
        email = user.email,
        role = user.role
        )    
    
    db.add(new_user)     # Add the new user to the session
    db.commit()          # Commit the transaction to the database
    db.refresh(new_user)
    return new_user

# Authenticate user and return token
@router.post("/login", 
             response_model = Token
             )
def login(db: Session = Depends(get_db),
          form_data: OAuth2PasswordRequestForm = Depends()
          ):
    """Authenticate user and return a JWT token."""

    db_user = db.query(User).filter(
        User.username == form_data.username
        ).first()
   
    if not db_user or not User.verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {"www-authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    # Generate token here
    access_token = create_access_token(
        data = {"sub":form_data.username}, 
        expires_delta=access_token_expires,
        )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }

@router.get("/{user_id}", response_model = UserRespone)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail= "User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

