from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from api.database import Base
from api.models import TimeStampMixin


class ChapterImageModel(Base, TimeStampMixin):
    __tablename__ = "chapter-images"

    id: Column[int] = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    image_url: Column[Text] = Column(Text)
    number: Column[int] = Column(Integer)
    chapter_id: Column[int] = Column(Integer, ForeignKey("chapters.id"))

    chapter = relationship("ChapterModel", back_populates="images")
