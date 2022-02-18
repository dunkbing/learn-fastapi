import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Text, UnicodeText
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from api.database import Base
from api.models import TimeStampMixin


class MangaStatus(enum.Enum):
    ongoing = 0
    completed = 1


class ChapterModel(Base, TimeStampMixin):
    __tablename__ = "chapters"

    id: Column[int] = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    title: Column[Text] = Column(UnicodeText, index=True)
    link: Column[Text] = Column(String, index=True)
    volume: Column[int] = Column(Integer, nullable=False)
    number: Column[int] = Column(Integer, nullable=False)
    manga_id: Column[int] = Column(Integer, ForeignKey("users.id"))

    manga = relationship("MangaModel", back_populates="chapters")
    chapter_images = relationship(
        "ChapterImageModel", back_populates="chapter")
