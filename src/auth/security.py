from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .exceptions import WrongPasswordException, InvalidTokenException
from ..database.core import get_db
from ..user.connector import get_user_by_username
from datetime import datetime, timedelta

from ..user.exceptions import UserNotFoundException, UserNotAdminException
from ..user.model import DBUser
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict

# Custom OAuth2PasswordBearer class that accepts access token from httpOnly Cookie
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")  #changed to accept access token from httpOnly Cookie
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")

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

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except JWTError:
        raise InvalidTokenException()

async def get_current_user(access_token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        username = decode_access_token(access_token)
        return get_user_by_username(db, username)
    except InvalidTokenException:
        raise InvalidTokenException()

async def get_current_admin(access_token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        username = decode_access_token(access_token)
        user = get_user_by_username(db, username)
        if user.privilege.name != "admin":
            raise UserNotAdminException()
        return user
    except InvalidTokenException:
        raise InvalidTokenException()