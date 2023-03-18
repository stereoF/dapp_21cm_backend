from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TEXT, DATETIME
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "user_info"

    addr = Column(String, primary_key=True, index=False)
    uname = Column(String)
    unit = Column(String)
    email = Column(String)
    admin = relationship("Admin", back_populates="user")


class Journal(Base):
    __tablename__ = "journal_infos"

    address = Column(String, primary_key=True, index=True)
    jname = Column(String, index=False)
    first_cate = Column(String)
    sec_cate = Column(String)
    third_cate = Column(String)
    subject_index = Column(Integer, autoincrement=True)
    remark = Column(TEXT)
    follow = relationship("Follow", back_populates="journal")


class Follow(Base):
    __tablename__ = "journal_follow"

    user_addr = Column(String, primary_key=True)
    journal_addr = Column(String, ForeignKey("journal_infos.address"), primary_key=True)
    journal = relationship("Journal", back_populates="follow")


class Admin(Base):
    __tablename__ = "journal_admins"

    user_addr = Column(String, ForeignKey("user_info.addr"), primary_key=True)
    type = Column(Integer)
    journal_addr = Column(String, ForeignKey("journal_infos.address"), primary_key=True)
    user = relationship("User", back_populates="admin")


class Article(Base):
    __tablename__ = "publication_infos"

    cid = Column(String, primary_key=True)
    author_addr = Column(String)
    c_status = Column(Integer)
    descs = Column(TEXT)
    title = Column(String)
    author_info = Column(String)
    abstract = Column(TEXT)
    submit_time = Column(DATETIME)
    prev_cid = Column(String)
    next_cid = Column(String)
    journal_addr = Column(String, ForeignKey("journal_infos.address"))
