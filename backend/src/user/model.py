from ..database.core import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
