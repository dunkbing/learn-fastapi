from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.user import services as user_services
from . import models


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.ItemModel).filter(models.ItemModel.id == item_id).first()


def get_item_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.ItemModel).filter(models.ItemModel.owner_id == user_id).offset(skip).limit(limit).all()


def get_items(db: Session, item_filter: models.ItemFilter, skip: int = 0, limit: int = 100):
    return db.query(models.ItemModel).offset(skip).limit(limit).all()
    # query = db.query(models.ItemModel)


def create_user_item(db: Session, item: models.ItemCreate):
    db_user = user_services.get_user_by_id(db, item.owner_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_item = models.ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
