from fastapi import APIRouter, Depends
from .connector import *
from .schemas import Group, GroupCreate

from ..database.core import get_db
from ..flashcard.schemas import Flashcard

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=list[Group])
def get_groups(db=Depends(get_db)):
    return get_all_groups(db)


@router.get("/{group_id}", response_model=Group)
def get_group(group_id: int, db=Depends(get_db)):
    try:
        group = get_group_by_id(db, group_id)
        return group
    except Exception as e:
        return {"error": str(e)}


@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db=Depends(get_db)):
    try:
        group = create_new_group(db, group.group_name, group.user_id)
        return group
    except Exception as e:
        return {"error": str(e)}


@router.put("/{group_id}")
def update_group(group_id: int, group: GroupCreate, db=Depends(get_db)):
    try:
        group = update_existing_group(db, group_id, group.name)
        return group
    except Exception as e:
        return {"error": str(e)}


@router.get("/{group_id}/flashcards", response_model=list[Flashcard])
def get_flashcards_in_group(group_id: int, db=Depends(get_db)):
    try:
        flashcards = get_all_flashcards_in_group(db, group_id)
        return flashcards
    except Exception as e:
        return {"error": str(e)}