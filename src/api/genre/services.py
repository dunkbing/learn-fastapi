from sqlalchemy.orm import Session
from . import models


def get_genre_by_id(db: Session, genre_id: int):
    return db.query(models.GenreModel).filter(models.GenreModel.id == genre_id).first()


def get_all_genres(db: Session):
    return db.query(models.GenreModel).all()


def create_genre(db: Session, genre: models.GenreCreate):
    db_genre = models.GenreModel(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre
