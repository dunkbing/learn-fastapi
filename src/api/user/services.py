from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from api.user.constants import ALGORITHM, SECRET_KEY
from api.utils.password import get_hashed_password, verify_password
from . import models


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def create_user(db: Session, user: models.UserCreate):
    fake_hashed_password = get_hashed_password(user.password)
    db_user = models.UserModel(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user_data: models.UserLogin):
    user = get_user_by_email(db, user_data.email)
    if not user:
        return False
    if not verify_password(user_data.password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
