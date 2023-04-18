from sqlalchemy import Boolean, Column, Integer, String, TEXT, DATETIME
from sqlalchemy.orm import relationship
from .database import Base
# from database import Base, engine


class User(Base):
    __tablename__ = "user_info"

    addr = Column(String(80), primary_key=True, index=False)
    uname = Column(String(80))
    unit = Column(String(100))
    email = Column(String(80))
    # admin = relationship("Admin", back_populates="user")


class Journal(Base):
    __tablename__ = "journal_infos"

    address = Column(String(80), primary_key=True, index=True)
    jname = Column(String(100), index=False)
    first_cate = Column(String(100))
    sec_cate = Column(String(100))
    third_cate = Column(String(100))
    subject_index = Column(Integer, autoincrement=True)
    remark = Column(TEXT)
    recommend = Column(Integer)
    journal_type = Column(String(80))
    # follow = relationship("Follow", back_populates="journal")


class Follow(Base):
    __tablename__ = "journal_follow"

    user_addr = Column(String(80), primary_key=True)
    # journal_addr = Column(String(80), ForeignKey("journal_infos.address"), primary_key=True)
    journal_addr = Column(String(80), primary_key=True)
    # journal = relationship("Journal", back_populates="follow")


class Admin(Base):
    __tablename__ = "journal_admins"

    # user_addr = Column(String(80), ForeignKey("user_info.addr"), primary_key=True)
    user_addr = Column(String(80), primary_key=True)
    type = Column(Integer)
    # journal_addr = Column(String(80), ForeignKey("journal_infos.address"), primary_key=True)
    journal_addr = Column(String(80), primary_key=True)
    # user = relationship("User", back_populates="admin")


class Article(Base):
    __tablename__ = "publication_infos"

    cid = Column(String(80), primary_key=True)
    author_addr = Column(String(80))
    c_status = Column(String(80))
    descs = Column(TEXT)
    title = Column(String(200))
    author_info = Column(String(200))
    abstract = Column(TEXT)
    submit_time = Column(DATETIME)
    prev_cid = Column(String(80))
    next_cid = Column(String(80))
    # journal_addr = Column(String(80), ForeignKey("journal_infos.address"))
    journal_addr = Column(String(80))



