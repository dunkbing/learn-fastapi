from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.item.models import Item, ItemCreate

from api.item import services

item_router = APIRouter()


@item_router.get("/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = services.get_items(db, skip=skip, limit=limit)
    return items


@item_router.post("/", response_model=Item, )
def create_item_for_user(item: ItemCreate, db: Session = Depends(get_db)):
    return services.create_user_item(db=db, item=item)
