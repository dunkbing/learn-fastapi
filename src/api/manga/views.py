from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from api.database import get_db
from .models import Manga, MangaCreate, MangaModel
from . import services

manga_router = APIRouter()


@manga_router.post("", response_model=Manga)
def create_manga(manga: MangaCreate, db: Session = Depends(get_db)):
    return services.create_manga(db=db, manga=manga)
