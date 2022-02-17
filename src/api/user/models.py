from sqlalchemy import Boolean, Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import TSVectorType
from pydantic import BaseModel

from api.database import Base
from api.item.models import Item
from api.models import TimeStampMixin


class UserModel(Base, TimeStampMixin):
    __tablename__ = "users"
    # __table_args__ = (Index("users_email_idx", "email"))

    id: Column[int] = Column(Integer, primary_key=True, index=True)
    email: Column[Text] = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("ItemModel", back_populates="owner")

    search_vector = Column(TSVectorType("email"))


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


UserLogin = UserCreate


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
