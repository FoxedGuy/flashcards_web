from ..database.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class DBFlashcard(Base):
    __tablename__ = "Flashcard"
    flashcard_id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"))

