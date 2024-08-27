from pydantic_settings.main import BaseModel


class GroupBase(BaseModel):
    group_name: str


class GroupCreate(GroupBase):
    user_id: int


class Group(GroupBase):
    group_id: int
    user_id: int

    class Config:
        orm_mode = True
