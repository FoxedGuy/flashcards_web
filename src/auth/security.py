from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .exceptions import WrongPasswordException, InvalidTokenException
from ..database.core import get_db
from ..user.connector import get_user_by_username
from datetime import datetime, timedelta

from ..user.exceptions import UserNotFoundException, UserNotAdminException
from ..user.model import DBUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user: DBUser = get_user_by_username(db,username)
    if user is None:
        raise UserNotFoundException()
    if not verify_password(password, user.password):
        raise WrongPasswordException()
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = get_user_by_username(db,username)
        if username is None:
            raise InvalidTokenException()
        return user
    except JWTError:
        raise InvalidTokenException()

async def get_current_admin(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = get_user_by_username(db,username)
        if username is None:
            raise InvalidTokenException()
        if user.privilege.name != "admin":
            raise UserNotAdminException()
        return user
    except JWTError:
        raise InvalidTokenException()