from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user_info"

    addr = Column(String, primary_key=True, index=False)
    uname = Column(String, unique=False, index=False)
    unit = Column(String)
    email = Column(String, default=False)
    type = Column(Integer)
    journal_addr = Column(String)
    # journal_info = relationship("Journal")


class Journal(Base):
    __tablename__ = "journal_infos"

    addr = Column(String, primary_key=True, index=True)
    jname = Column(String, index=False)
    first_cate = Column(String)
    sec_cate = Column(String)
    third_cate = Column(String)
    subject_index = Column(Integer)
    remark = Column(String)

#
# class Follow(Base):
#     __tablename__ = "journal_follow"
#
#     user_addr = Column(String)
#     journal_add = Column(String)
#     journals = relationship("Journal")
