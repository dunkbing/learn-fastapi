from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from api.database import Base
from api.models import TimeStampMixin


class GenreModel(Base, TimeStampMixin):
    __tablename__ = "genres"

    id: Column[int] = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    name: Column[Text] = Column(Text, index=True)


class Genre(BaseModel):
    id: int
    name: str
