from sqlalchemy.orm import relationship
from ..database.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class DBPrivilege(Base):
    __tablename__ = "privileges"
    privilege_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True)

class DBUser(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
    groups = relationship("DBGroup", back_populates="user")
    privilege_id = Column(Integer, ForeignKey('privileges.privilege_id'))
    privilege = relationship("DBPrivilege")