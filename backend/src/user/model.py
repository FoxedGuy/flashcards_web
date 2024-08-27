from sqlalchemy.orm import relationship

from ..database.core import Base
from sqlalchemy import Column, Integer, String


class DBUser(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
    groups = relationship("DBGroup", back_populates="user")
