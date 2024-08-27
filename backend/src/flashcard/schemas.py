from pydantic_settings.main import BaseModel


class FlashcardBase(BaseModel):
    question: str
    answer: str


class FlashcardCreate(FlashcardBase):
    user_id: int


class Flashcard(FlashcardBase):
    flashcard_id: int
    user_id: int

    class Config:
        orm_mode = True
