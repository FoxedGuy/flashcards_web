from ..database.core import get_db
from fastapi import APIRouter, Depends
from .schemas import User, UserCreate
from .connector import *
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def get_users(db=Depends(get_db)):
    return get_all_users(db)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db=Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        return user
    except Exception as e:
        return {"error": str(e)}


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        user = create_new_user(db, user.username, user.password, user.email)
        return user
    except Exception as e:
        return {"error": str(e)}


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate, db=Depends(get_db)):
    try:
        user = update_existing_user(db, user_id, user.username, user.password, user.email)
        return user
    except Exception as e:
        return {"error": str(e)}