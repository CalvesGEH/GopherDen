from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm.session import Session

from db.database import get_db
from sqlalchemy.orm import Session
from db.models import User, Chore
from schema.schemas import UserSchema, UserCreateSchema

router = APIRouter(prefix="/user")

# Example endpoint to get all users
@router.get("")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{username}/chores")
def get_chores(username, db: Session = Depends(get_db)):
    cur_user = db.query(User).filter(User.username == username).all()
    return cur_user[0].chores

# Example endpoint to create a user
@router.post("", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user