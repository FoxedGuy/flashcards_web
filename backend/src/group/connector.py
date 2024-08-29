from .model import DBGroup
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_all_groups(db: Session):
    return db.query(DBGroup).all()


def get_group_by_id(db: Session, group_id: int):
    group = db.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


def create_new_group(db: Session, group_name: str, user_id: int):
    new_group = DBGroup(group_name=group_name, user_id=user_id)
    db.add(new_group)
    db.commit()

    return new_group


def update_existing_group(db: Session, group_id: int, group_name: str | None):
    group = db.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    if group_name:
        group.group_name = group_name

    db.commit()

    return group


def get_all_flashcards_in_group(db: Session, group_id: int):
    group = db.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    return group.flashcards
