from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from api.database import Base
from api.models import CamelModel, TimeStampMixin


class GenreModel(Base, TimeStampMixin):
    __tablename__ = "genres"

    id: Column[int] = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    name: Column[Text] = Column(Text, index=True)


class Genre(CamelModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GenreCreate(BaseModel):
    name: str
