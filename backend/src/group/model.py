from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database.core import Base


class DBGroup(Base):
    __tablename__ = "Group"
    group_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    group_name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    user = relationship("DBUser", back_populates="groups")
    flashcards = relationship("DBFlashcard")
