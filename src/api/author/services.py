from sqlalchemy.orm import Session
from . import models


def get_author_by_id(db: Session, id: int):
    return db.query(models.AuthorModel).filter(models.AuthorModel.id == id).first()


def get_all_authors(db: Session):
    return db.query(models.AuthorModel).all()


def create_author(db: Session, genre: models.AuthorCreate):
    db_author = models.AuthorModel(**genre.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
