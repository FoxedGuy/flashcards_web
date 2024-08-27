from .model import DBFlashcard
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..user.model import DBUser


def get_all_flashcards(db: Session):
    return db.query(DBFlashcard).all()


def get_flashcard_by_id(db: Session, flashcard_id: int):
    flashcard = db.query(DBFlashcard).filter(DBFlashcard.flashcard_id == flashcard_id).first()

    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    return flashcard


def create_new_flashcard(db: Session, question: str, answer: str, user_id: int):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_flashcard = DBFlashcard(question=question, answer=answer, user_id=user_id)
    db.add(new_flashcard)
    db.commit()

    return new_flashcard


def update_existing_flashcard(db: Session, flashcard_id: int, question: str | None, answer: str | None, user_id: int | None):
    flashcard = db.query(DBFlashcard).filter(DBFlashcard.flashcard_id == flashcard_id).first()

    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    if question:
        flashcard.question = question

    if answer:
        flashcard.answer = answer

    if user_id:
        flashcard.user_id = user_id

    db.commit()

    return flashcard

