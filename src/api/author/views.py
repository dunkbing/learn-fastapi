from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from . import services
from . import models

author_router = APIRouter()


@author_router.post("", response_model=models.Author)
def create_author(author: models.AuthorCreate, db: Session = Depends(get_db)):
    return services.create_author(db=db, genre=author)


@author_router.get("/{author_id}", response_model=models.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return services.get_author_by_id(db=db, id=author_id)


@author_router.get("", response_model=list[models.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return services.get_all_authors(db=db)
