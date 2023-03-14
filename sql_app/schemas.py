from typing import List

from pydantic import BaseModel


class JournalBase(BaseModel):
    addr: str
    jname: str
    first_cate: str
    sec_cate: str
    third_cate: str
    remark: str


class JournalCreate(JournalBase):
    subject_index: int


class Journal(JournalBase):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    addr: str
    uname: str
    unit: str
    email: str
    type: int
    journal_addr: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    # journal_infos: Journal

    class Config:
        orm_mode = True


class FollowBase(BaseModel):
    user_addr: str
    journal_addr: str


class FollowCreate(FollowBase):
    pass


class Follow(FollowBase):
    pass