from decimal import Decimal
import enum
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import TSVectorType
from pydantic import BaseModel

from api.database import Base
from api.models import TimeStampMixin


class MangaStatus(enum.Enum):
    ongoing = 0
    completed = 1


manga_author_table = Table(
    'mangas_authors',
    Base.metadata,
    Column('manga_id', Integer, ForeignKey('manga.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True))

manga_genre_table = Table(
    'mangas_genres',
    Base.metadata,
    Column('manga_id', Integer, ForeignKey('manga.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True))


class MangaModel(Base, TimeStampMixin):
    __tablename__ = "mangas"

    id: Column[int] = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    title: Column[Text] = Column(String, index=True)
    alt_title: Column[Text] = Column(String, index=True, nullable=True)
    rating: Column[Decimal] = Column(Float, nullable=True)
    thumbnail: Column[Text] = Column(String, nullable=True)
    image: Column[Text] = Column(String, nullable=True)
    description: Column[Text] = Column(Text)
    source: Column[Text] = Column(Text, nullable=True)
    source_url: Column[Text] = Column(Text, nullable=True)
    status = Column(Enum(MangaStatus), nullable=True)
    year: Column[int] = Column(Integer, nullable=True)
    updated_detail: Column[Text] = Column(Text, nullable=True)
    updated_chapters: Column[Text] = Column(Integer, nullable=True)

    chapters = relationship("ChapterModel", back_populates="manga")
    authors = relationship(
        "AuthorModel", secondary=manga_author_table, backref="mangas")
    genres = relationship(
        "GenreModel", secondary=manga_genre_table, backref="mangas")

    search_vector = Column(TSVectorType("title", "alt_title"))
