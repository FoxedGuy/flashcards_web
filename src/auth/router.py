from fastapi.security import OAuth2PasswordRequestForm

from .schemas import RegisterForm
from ..database.core import get_db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from ..auth.security import authenticate_user, create_access_token
from datetime import timedelta
from jose import JWTError, jwt
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, oauth2_scheme
from ..user.connector import get_user_by_username, create_new_user, check_if_user_exists

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
async def register_new_user(form_data: RegisterForm, db=Depends(get_db)):
    name_taken: bool = check_if_user_exists(db, form_data.username)
    if name_taken:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = create_new_user(db, form_data.username, form_data.password, form_data.email)
    return user
