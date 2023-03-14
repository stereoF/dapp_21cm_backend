from fastapi import APIRouter, HTTPException, Depends
from sql_app import schemas, crud
from sqlalchemy.orm import Session

from ..dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{user_addr}", response_model=schemas.User)
def user_infos(user_addr: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_addr=user_addr)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user