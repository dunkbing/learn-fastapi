from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from . import services
from . import models

genre_router = APIRouter()


@genre_router.post("", response_model=models.Genre)
def create_genre(genre: models.GenreCreate, db: Session = Depends(get_db)):
    return services.create_genre(db=db, genre=genre)


@genre_router.get("", response_model=list[models.Genre])
def get_all_genres(db: Session = Depends(get_db)):
    return services.get_all_genres(db=db)
