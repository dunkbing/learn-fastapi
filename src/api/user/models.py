from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel

from api.database import Base
from api.item.models import Item


class UserModel(Base):
    __tablename__ = "users"

    id: Column[int] = Column(Integer, primary_key=True, index=True)
    email: Column[Text] = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("ItemModel", back_populates="owner")


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
