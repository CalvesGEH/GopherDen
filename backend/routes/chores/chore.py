from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from db.database import get_db
from schema.schemas import ChoreCreateSchema, ChoreSchema
from db.models import Chore

router = APIRouter(prefix="/chore")

@router.post("/", response_model=ChoreSchema)
def create_chore(chore: ChoreCreateSchema, db: Session = Depends(get_db)):
    db_chore = Chore(name=chore.name, description=chore.description, assigned_to_id=chore.assigned_to_id, completed=chore.completed)
    db.add(db_chore)
    db.commit()
    db.refresh(db_chore)
    return db_chore

@router.get("/all", response_model=list[ChoreSchema])
def read_chores(db: Session = Depends(get_db)):
    chores = db.query(Chore).all()
    return chores