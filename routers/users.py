from fastapi import  Depends, FastAPI, HTTPException, Query,APIRouter
from sql_app import schemas, crud
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List
import sys
from pydantic import Required

sys.path.append("..")

router = APIRouter()


@router.get("/admin/user_addr={user_addr}&journal_addr={journal_addr}", response_model=schemas.Admin)
def user_info(user_addr: str, journal_addr: str, db: Session = Depends(get_db)):
    admin = crud.get_admin(db, user_addr=user_addr, journal_addr=journal_addr)
    if admin is None:
        raise HTTPException(status_code=404, detail="unknown admin")
    return admin


@router.get("/admin/reviewer/journal_addr={journal_addr}", response_model=List[schemas.Admin])
def user_info(journal_addr: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviewers = crud.get_reviewers(db, journal_addr=journal_addr, skip=skip, limit=limit)
    if reviewers is None:
        raise HTTPException(status_code=404, detail="reviewers not found")
    return reviewers


@router.get("/follow/{user_addr}", response_model=List[schemas.Follow])
def user_follow_info(user_addr: str, db: Session = Depends(get_db)):
    journals = crud.get_user_follow(db, user_addr=user_addr)
    if journals is None:
        raise HTTPException(status_code=404, detail="follow not found")
    return journals


@router.get("/journal/info", response_model=List[schemas.Journal])
def journal_info(db: Session = Depends(get_db)):
    journals = crud.get_journals(db)
    if journals is None:
        raise HTTPException(status_code=404, detail="journal not found")
    return journals


@router.post("/user/create", response_model=schemas.User)
def journal_info(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user)
    if user is None:
        raise HTTPException(status_code=404, detail="user add error")
    return user


@router.post("/journal/create", response_model=schemas.Journal)
def journal_info(journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    journal = crud.create_journal(db, journal)
    if journal is None:
        raise HTTPException(status_code=404, detail="journal add error")
    return journal


@router.post("/follow/create", response_model=schemas.Follow)
def journal_info(follow: schemas.FollowCreate, db: Session = Depends(get_db)):
    follow = crud.create_follow(db, follow)
    if follow is None:
        raise HTTPException(status_code=404, detail="follow add error")
    return follow


@router.post("/admin/create", response_model=schemas.Admin)
def journal_info(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    admin = crud.create_admin(db, admin)
    if admin is None:
        raise HTTPException(status_code=404, detail="admin add error")
    return admin


@router.get("/article/info", response_model=List[schemas.Article])
def article_info(cid: str = Query(default=None), author_addr: str = Query(default=None),
                 status: int = Query(default=None), journal_addr: str = Query(default=Required),
                 skip: int = Query(default=0), limit: int = Query(default=10),
                 db: Session = Depends(get_db)):
    articles = crud.get_articles(db, cid, author_addr, status, journal_addr, skip, limit)
    if articles is None:
        raise HTTPException(status_code=404, detail="articles not found")
    return articles


@router.post("/article/create", response_model=schemas.Article)
def article_info(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = crud.create_articles(db, article)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    return article
