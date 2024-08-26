from .model import DBUser
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_all_users(db: Session):
    return db.query(DBUser).all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_new_user(db: Session, username: str, password: str, email: str):
    check_user = db.query(DBUser).filter(DBUser.username == username).first()
    if check_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    check_email = db.query(DBUser).filter(DBUser.email == email).first()
    if check_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = DBUser(username=username, password=password, email=email)
    db.add(new_user)
    db.commit()

    return new_user


def update_existing_user(db: Session, user_id: int, username: str | None, password: str | None, email: str | None):
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
        user.password = password

    db.commit()

    return user
