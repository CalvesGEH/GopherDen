# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    completed = Column(Boolean, default=False)

    # Relationship to User
    assigned_to = relationship("User", back_populates="chores")

# Add the reverse relationship in the User model
User.chores = relationship("Chore", order_by=Chore.id, back_populates="assigned_to")