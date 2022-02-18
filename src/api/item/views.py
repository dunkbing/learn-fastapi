from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.item.models import Item, ItemCreate, ItemFilter

from api.item import services

item_router = APIRouter()


@item_router.get("", response_model=list[Item])
def read_items(item_filter: ItemFilter, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = services.get_items(db, item_filter, skip=skip, limit=limit)
    return items


@item_router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = services.get_item_by_id(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@item_router.get("/user/{user_id}", response_model=list[Item])
def read_items_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = services.get_item_by_user_id(
        db, user_id=user_id, skip=skip, limit=limit)
    return items


@item_router.post("", response_model=Item, )
def create_item_for_user(item: ItemCreate, db: Session = Depends(get_db)):
    return services.create_user_item(db=db, item=item)
