from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import TSVectorType

from api.database import Base


class ItemModel(Base):
    __tablename__ = "items"
    # __table_args__ = (Index("items_title_idx", "title"))

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id: Column[int] = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="items")

    search_vector = Column(TSVectorType("title"))


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    owner_id: int


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemFilter(BaseModel):
    title: str
