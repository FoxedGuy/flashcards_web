from pydantic_settings.main import BaseModel
from ..group.schemas import Group


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    groups: list[Group]

    class Config:
        orm_mode = True
