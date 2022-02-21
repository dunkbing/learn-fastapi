from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from . import services
from . import models

chapter_image_router = APIRouter()


@chapter_image_router.get("", response_model=list[models.ChapterImage])
def get_images_by_chapter_id(chapter_id: int, db: Session = Depends(get_db)):
    return services.get_images_by_chapter_id(db=db, chapter_id=chapter_id)
