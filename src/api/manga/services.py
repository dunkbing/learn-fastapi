from sqlalchemy.orm import Session
from . import models
from api.author import models as author_models


def create_manga(db: Session, manga_create: models.MangaCreate):
    db_manga = models.MangaModel(
        title=manga_create.title,
        alt_title=manga_create.alt_title,
        rating=manga_create.rating,
        thumbnail=manga_create.thumbnail,
        image=manga_create.image,
        description=manga_create.description,
        source=manga_create.source,
        source_url=manga_create.source_url,
        status=manga_create.status,
        year=manga_create.year,
        updated_detail=manga_create.updated_detail,
        updated_chapters=manga_create.updated_chapters,
    )
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga


def get_manga_by_id(db: Session, manga_id: int):
    return db.query(models.MangaModel).filter(models.MangaModel.id == manga_id).first()


def search_manga(db: Session, title_or_author: str):
    query = db.query(models.MangaModel).join(author_models.AuthorModel).filter(
        models.MangaModel.search_vector.match(title_or_author) |
        author_models.AuthorModel.search_vector.match(title_or_author)
    )

    return query.all()
