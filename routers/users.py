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
def user_journal_role(user_addr: str, journal_addr: str, db: Session = Depends(get_db)):
    """
    进入期刊后，获取用户在该期刊中的角色（分为None：无角色，0：管理员；1：编辑；2：审稿人），根据角色展示页面内容
    :param user_addr: 用户地址
    :param journal_addr: 期刊地址
    :param db: mysql session
    :return:
    """
    admin = crud.get_admin(db, user_addr=user_addr, journal_addr=journal_addr)
    return admin


@router.get("/admin/reviewer/journal_addr={journal_addr}", response_model=List[schemas.Admin])
def reviewer_info(journal_addr: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    期刊编辑获取该期刊的审稿人列表，方便进行分配审稿人的操作
    :param journal_addr: 期刊合约地址
    :param skip: 开始位置
    :param limit: 显示数量
    :param db: mysql session
    :return:
    """
    reviewers = crud.get_reviewers(db, journal_addr=journal_addr, skip=skip, limit=limit)
    if reviewers is None:
        raise HTTPException(status_code=404, detail="reviewers not found")
    return reviewers


@router.get("/follow/{user_addr}", response_model=List[schemas.Follow])
def user_follow_info(user_addr: str, db: Session = Depends(get_db)):
    """
    展示用户关注的期刊信息，方便用户选择期刊进入对应期刊
    :param user_addr: 用户地址
    :param db:
    :return:
    """
    journals = crud.get_user_follow(db, user_addr=user_addr)
    if journals is None:
        raise HTTPException(status_code=404, detail="follow not found")
    return journals


@router.get("/journal/info", response_model=List[schemas.Journal])
def journal_info(db: Session = Depends(get_db)):
    """
    所有的合约地址及详细信息，用户可以选择其中一个进入或关注
    :param db:
    :return:
    """
    journals = crud.get_journals(db)
    if journals is None:
        raise HTTPException(status_code=404, detail="journal not found")
    return journals


@router.post("/user/create", response_model=schemas.User)
def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    新建编辑或者审稿人信息
    :param user:
    :param db:
    :return:
    """
    user = crud.create_user(db, user)
    if user is None:
        raise HTTPException(status_code=404, detail="user add error")
    return user


@router.post("/journal/create", response_model=schemas.Journal)
def journal_create(journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    """
    添加期刊合约详细信息
    :param journal:
    :param db:
    :return:
    """
    journal = crud.create_journal(db, journal)
    if journal is None:
        raise HTTPException(status_code=404, detail="journal add error")
    return journal


@router.post("/follow/create", response_model=schemas.Follow)
def follow_create(follow: schemas.FollowCreate, db: Session = Depends(get_db)):
    """
    用户关注期刊操作
    :param follow:
    :param db:
    :return:
    """
    follow = crud.create_follow(db, follow)
    if follow is None:
        raise HTTPException(status_code=404, detail="follow add error")
    return follow


@router.post("/admin/create", response_model=schemas.Admin)
def admin_create(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    """
    将用户（已在用户表中）设置为期刊的编辑和审稿人
    :param admin:
    :param db:
    :return:
    """
    admin = crud.create_admin(db, admin)
    if admin is None:
        raise HTTPException(status_code=404, detail="admin add error")
    return admin


@router.get("/article/info", response_model=List[schemas.Article])
def article_info(cid: str = Query(default=None), author_addr: str = Query(default=None),
                 status: str = Query(default='Pending'), journal_addr: str = Query(default=Required),
                 skip: int = Query(default=0), limit: int = Query(default=10),
                 db: Session = Depends(get_db)):
    """
    展示文章信息，可以根据cid查询，合约地址查询，文章状态，文章作者等，配置不同的条件即可
    :param cid:
    :param author_addr:
    :param status:
    :param journal_addr:
    :param skip:
    :param limit:
    :param db:
    :return:
    """
    articles = crud.get_articles(db, cid, author_addr, status, journal_addr, skip, limit)
    if articles is None:
        raise HTTPException(status_code=404, detail="articles not found")
    return articles


@router.post("/article/create", response_model=schemas.Article)
def article_create(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """
    新建稿件信息
    :param article:
    :param db:
    :return:
    """
    article = crud.create_articles(db, article)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    return article
