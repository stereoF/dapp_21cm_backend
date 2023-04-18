from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def get_admin(db: Session, user_addr: str, journal_addr: str):
    return db.query(models.Admin).filter(models.Admin.user_addr == user_addr,
                                         models.Admin.journal_addr == journal_addr).first()


def get_reviewers(db: Session, journal_addr: str, skip: int = 0, limit: int = 10):
    return db.query(models.Admin).filter(models.Admin.type == 2,
                                         models.Admin.journal_addr == journal_addr).offset(skip).limit(limit).all()


def get_user_follow(db: Session, user_addr: str, skip: int = 0, limit: int = 10):
    return db.query(models.Follow).filter(models.Follow.user_addr == user_addr).offset(skip).limit(limit).all()


def get_journals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Journal).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(addr=user.addr, uname=user.uname, email=user.email, unit=user.unit)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_follow(db: Session, follow: schemas.FollowCreate):
    db_follow = models.Follow(user_addr=follow.user_addr, journal_addr=follow.journal_addr)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def create_journal(db: Session, journal: schemas.JournalCreate):
    db_journal = models.Journal(address=journal.address, jname=journal.jname, first_cate=journal.first_cate,
                                sec_cate=journal.sec_cate, third_cate=journal.third_cate,
                                remark=journal.remark)
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal


def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(user_addr=admin.user_addr, type=admin.type, journal_addr=admin.journal_addr)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_articles(db: Session, cid: str, author_addr: str, status: str, journal_addr: str, skip: int, limit: int):
    return db.query(models.Article).filter(models.Article.cid == cid if cid is not None else 1 == 1,
                                           models.Article.author_addr == author_addr if author_addr is not None else 1 == 1,
                                           models.Article.c_status == status if status is not None else 1 == 1,
                                           models.Article.journal_addr == journal_addr).offset(skip).limit(limit).all()


def create_articles(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(cid=article.cid,
                                author_addr=article.author_addr,
                                c_status=article.c_status,
                                descs=article.descs,
                                title=article.title,
                                author_info=article.author_info,
                                abstract=article.abstract,
                                submit_time=article.submit_time,
                                prev_cid=article.prev_cid,
                                next_cid=article.next_cid,
                                journal_addr=article.journal_addr)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article_by_cid(db: Session, cid: str, journal_addr: str):
    return db.query(models.Article).filter(models.Article.cid == cid, models.Article.journal_addr == journal_addr).first()
