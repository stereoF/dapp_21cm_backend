from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_addr: str):
    return db.query(models.User).filter(models.User.addr == user_addr).first()


# def get_user_follow(db: Session, user_addr: str, skip: int = 0, limit: int = 10):
#     return db.query(models.Follow).filter(models.Follow.user_addr == user_addr).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(addr=user.addr, uname=user.uname, email=user.email, unit=user.unit, type=user.type,
                          journal_addr=user.journal_addr)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
