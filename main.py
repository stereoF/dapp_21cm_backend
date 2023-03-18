from fastapi import FastAPI, UploadFile, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from pydantic import Required
from sql_app import schemas, models, crud
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    # "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file.filename)
    return {"filename": file.filename}


@app.get("/admin/user_addr={user_addr}&journal_addr={journal_addr}", response_model=schemas.Admin)
def user_info(user_addr: str, journal_addr: str, db: Session = Depends(get_db)):
    admin = crud.get_admin(db, user_addr=user_addr, journal_addr=journal_addr)
    if admin is None:
        raise HTTPException(status_code=404, detail="unknown admin")
    return admin


@app.get("/admin/reviewer/journal_addr={journal_addr}", response_model=List[schemas.Admin])
def user_info(journal_addr: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviewers = crud.get_reviewers(db, journal_addr=journal_addr, skip=skip, limit=limit)
    if reviewers is None:
        raise HTTPException(status_code=404, detail="reviewers not found")
    return reviewers


@app.get("/follow/{user_addr}", response_model=List[schemas.Follow])
def user_follow_info(user_addr: str, db: Session = Depends(get_db)):
    journals = crud.get_user_follow(db, user_addr=user_addr)
    if journals is None:
        raise HTTPException(status_code=404, detail="follow not found")
    return journals


@app.get("/journal/info", response_model=List[schemas.Journal])
def journal_info(db: Session = Depends(get_db)):
    journals = crud.get_journals(db)
    if journals is None:
        raise HTTPException(status_code=404, detail="journal not found")
    return journals


@app.post("/user/create", response_model=schemas.User)
def journal_info(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user)
    if user is None:
        raise HTTPException(status_code=404, detail="user add error")
    return user


@app.post("/journal/create", response_model=schemas.Journal)
def journal_info(journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    journal = crud.create_journal(db, journal)
    if journal is None:
        raise HTTPException(status_code=404, detail="journal add error")
    return journal


@app.post("/follow/create", response_model=schemas.Follow)
def journal_info(follow: schemas.FollowCreate, db: Session = Depends(get_db)):
    follow = crud.create_follow(db, follow)
    if follow is None:
        raise HTTPException(status_code=404, detail="follow add error")
    return follow


@app.post("/admin/create", response_model=schemas.Admin)
def journal_info(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    admin = crud.create_admin(db, admin)
    if admin is None:
        raise HTTPException(status_code=404, detail="admin add error")
    return admin


@app.get("/article/info", response_model=List[schemas.Article])
def article_info(cid: str = Query(default=None), author_addr: str = Query(default=None),
                 status: int = Query(default=None), journal_addr: str = Query(default=Required),
                 skip: int = Query(default=0), limit: int = Query(default=10),
                 db: Session = Depends(get_db)):
    articles = crud.get_articles(db, cid, author_addr, status, journal_addr, skip, limit)
    if articles is None:
        raise HTTPException(status_code=404, detail="articles not found")
    return articles


@app.post("/article/create", response_model=schemas.Article)
def article_info(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = crud.create_articles(db, article)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    return article
