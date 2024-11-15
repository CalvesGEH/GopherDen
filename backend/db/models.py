from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from slugify import slugify

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users_table"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    password: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)

    chores: Mapped[List["ChoreModel"]] = relationship(back_populates="user", cascade='all, delete', uselist=True)

class ChoreModel(Base):
    __tablename__ = "chores_table"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    slug: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]]
    total_time: Mapped[Optional[str]]
    frequency: Mapped[Optional[str]]

    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    user: Mapped[UserModel] = relationship(back_populates="chores")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slug = slugify(self.name)