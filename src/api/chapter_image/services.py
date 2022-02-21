from sqlalchemy.orm import Session
from . import models


def get_images_by_chapter_id(db: Session, chapter_id: int):
    query = db.query(models.ChapterImageModel).filter(
        models.ChapterImageModel.chapter_id == chapter_id)
    return query.all()
