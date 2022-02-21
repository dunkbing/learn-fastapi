from sqlalchemy.orm import Session
from . import models


def get_all_genres(db: Session):
    return db.query(models.GenreModel).all()
