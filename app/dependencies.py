from fastapi import Depends, HTTPException, status
from routers.user import get_current_user

from database import get_db
from models import User
from enums import UserRole

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

# def role_required(required_role: UserRole):
#     def role_checker(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
#         credentials_exception = HTTPException(
#             status_code = status.HTTP_401_UNAUTHORIZED,
#             detail = "could not validate credentials",
#             headers = {"WWW-Authenticate":"Bearer"},
#         )
#         try:
#             payload = jwt.encode(token, SECRET_KEY, algorithms = [ALGORITHM])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise credentials_exception
#             user = db.query(User).filter(User.username == username).first()
#             if user is None or user.role != required_role:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail ="Not enough permissions",
#                 )
#         except JWTError:
#             raise credentials_exception

#         return user

#     return role_checker

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