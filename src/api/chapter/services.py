from sqlalchemy.orm import Session
from . import models
from api.author import models as author_models


def get_chapters_by_manga_id(db: Session, manga_id: int, skip: int = 0, limit: int = 100):
    query = db.query(models.ChapterModel).filter(
        models.ChapterModel.manga_id == manga_id)
    return query.offset(skip).limit(limit).all()
