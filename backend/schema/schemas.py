# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List

class UserBaseSchema(BaseModel):
    username: str
    email: str

class UserCreateSchema(UserBaseSchema):
    pass

class UserSchema(UserBaseSchema):
    id: int
    chores: List['ChoreSchema'] = []

    class Config:
        from_attributes=True

class ChoreBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    assigned_to_id: int
    completed: bool = False

class ChoreCreateSchema(ChoreBaseSchema):
    pass

class ChoreSchema(ChoreBaseSchema):
    id: int

    class Config:
        from_attributes=True