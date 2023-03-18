from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class JournalBase(BaseModel):
    address: str
    jname: str
    first_cate: str
    sec_cate: str
    third_cate: str
    remark: Union[str, None] = None


class JournalCreate(JournalBase):
    pass


class Journal(JournalBase):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    addr: str
    uname: str
    unit: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    class Config:
        orm_mode = True


class FollowBase(BaseModel):
    user_addr: str
    journal_addr: str


class FollowCreate(FollowBase):
    pass


class Follow(FollowBase):
    journal: Journal

    class Config:
        orm_mode = True


class AdminBase(BaseModel):
    user_addr: str
    type: int
    journal_addr: str


class AdminCreate(AdminBase):
    pass


class Admin(AdminBase):
    user: User

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    cid: str
    author_addr: str
    c_status: int
    descs: str
    title: str
    author_info: str
    abstract: str
    submit_time: datetime
    prev_cid: str
    next_cid: str
    journal_addr: str


class Article(ArticleBase):
    class Config:
        orm_mode = True


class ArticleCreate(ArticleBase):
    pass
