from fastapi import APIRouter, Depends
from ..database.core import get_db
from .connector import *
from .schemas import Flashcard, FlashcardCreate


router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/", response_model=list[Flashcard])
async def get_flashcards(db=Depends(get_db)):
    return get_all_flashcards(db)


@router.get("/{flashcard_id}", response_model=Flashcard)
async def get_flashcard(flashcard_id: int, db=Depends(get_db)):
    try:
        flashcard = get_flashcard_by_id(db, flashcard_id)
        return flashcard
    except Exception as e:
        return {"error": str(e)}


@router.post("/", response_model=Flashcard)
async def create_flashcard(flashcard: FlashcardCreate, db=Depends(get_db)):
    try:
        flashcard = create_new_flashcard(db, flashcard.question, flashcard.answer, flashcard.user_id, flashcard.group_id)
        return flashcard
    except Exception as e:
        return {"error": str(e)}


@router.put("/{flashcard_id}")
async def update_flashcard(flashcard_id: int, flashcard: FlashcardCreate, db=Depends(get_db)):
    try:
        flashcard = update_existing_flashcard(db, flashcard_id, flashcard.question, flashcard.answer, flashcard.user_id)
        return flashcard
    except Exception as e:
        return {"error": str(e)}