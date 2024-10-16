from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

from models import User
from schemas import UserCreate, UserRespone, Token, TokenData
from database import get_db

router = APIRouter()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
SECRET_KEY = "e42b5e344b86122fa23469990d9dc73a445860b8fd13e1f3bff398990a58d635"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

@router.get("/users/me",
            response_model=UserRespone
            )
def read_users_me(
    current_user: UserCreate = Depends(get_current_user)
    ):
    return current_user

