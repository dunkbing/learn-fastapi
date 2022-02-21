from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from api.database import get_db
from .models import Chapter
from . import services

chapter_router = APIRouter()


@chapter_router.get("", response_model=list[Chapter])
def get_all_chapters(manga_id: int, db: Session = Depends(get_db)):
    return services.get_chapters_by_manga_id(db=db, manga_id=manga_id)
