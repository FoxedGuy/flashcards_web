from .model import DBUser, DBPrivilege
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session):
    return db.query(DBUser).all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_new_user(db: Session, username: str, password: str, email: str, privilege_id: int | None = None):
    check_user = db.query(DBUser).filter(DBUser.username == username).first()
    if check_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    check_email = db.query(DBUser).filter(DBUser.email == email).first()
    if check_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(password)
    if privilege_id is None:
        privilege_id = db.query(DBPrivilege).filter(DBPrivilege.name == "user").first().privilege_id

    new_user = DBUser(username=username, password=hashed_password, email=email, privilege_id=privilege_id)
    db.add(new_user)
    db.commit()

    return new_user


def update_existing_user(db: Session, user_id: int, username: str | None, password: str | None, email: str | None, privilege_id: int | None):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        check_user = db.query(DBUser).filter(DBUser.username == username).first()
        if check_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        user.username = username

    if email:
        check_email = db.query(DBUser).filter(DBUser.email == email).first()
        if check_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = email

    if password:
        user.password = pwd_context.hash(password)

    if privilege_id:
        user.privilege_id = privilege_id

    db.commit()

    return user

def delete_user_by_id(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()