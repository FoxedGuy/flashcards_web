from ..database.core import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "Users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)
