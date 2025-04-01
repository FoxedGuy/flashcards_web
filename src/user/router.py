from ..auth.security import get_current_user, get_current_admin
from ..database.core import get_db
from fastapi import APIRouter, Depends
from .schemas import User, UserCreate
from .connector import *
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def get_users(db=Depends(get_db), current_user_admin = Depends(get_current_admin)):
    return get_all_users(db)

@router.get("/me")
async def read_users_me(db=Depends(get_db), current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db=Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        return user
    except UserNotFoundException:
        raise UserNotFoundException()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        user = create_new_user(db, user.username, user.password, user.email)
        return user
    except UserAlreadyExistsException:
        raise UserAlreadyExistsException()
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException()

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate, db=Depends(get_db)):
    try:
        user = update_existing_user(db, user_id, user.username, user.password, user.email)
        return user
    except UserNotFoundException:
        raise UserNotFoundException()
    except UserAlreadyExistsException:
        raise UserAlreadyExistsException()
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException()

@router.delete("/{user_id}")
async def delete_user(user_id: int, db=Depends(get_db)):
    try:
        delete_user_by_id(db, user_id)
        return {'message': 'User deleted successfully'}
    except Exception as e:
        return {"error": str(e)}
