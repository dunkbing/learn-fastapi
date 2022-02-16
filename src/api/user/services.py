from sqlalchemy.orm import Session

from api.utils.password import get_hashed_password
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: models.UserCreate):
    fake_hashed_password = get_hashed_password(user.password)
    db_user = models.UserModel(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
