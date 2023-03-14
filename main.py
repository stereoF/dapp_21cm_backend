from fastapi import FastAPI, UploadFile, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session

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


@app.get("/users/{user_addr}", response_model=schemas.User)
def user_infos(user_addr: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_addr=user_addr)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file.filename)
    return {"filename": file.filename}
