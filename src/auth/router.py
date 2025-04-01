from fastapi.security import OAuth2PasswordRequestForm

from .exceptions import WrongPasswordException
from .schemas import RegisterForm
from ..database.core import get_db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from ..auth.security import authenticate_user, create_access_token
from ..user.exceptions import UserAlreadyExistsException, UserNotFoundException, EmailAlreadyExistsException
from datetime import timedelta
from .security import ACCESS_TOKEN_EXPIRE_MINUTES
from ..user.connector import create_new_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    try:
        user = authenticate_user(db,form_data.username, form_data.password)
    except UserNotFoundException:
        raise UserNotFoundException()
    except WrongPasswordException:
        raise WrongPasswordException()
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
async def register_new_user(form_data: RegisterForm, db=Depends(get_db)):
    try:
        user = create_new_user(db, form_data.username, form_data.password, form_data.email)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsException()
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException()
    return user
