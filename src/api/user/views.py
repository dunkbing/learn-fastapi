from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .models import User, UserCreate
from api.database import get_db
from api.user import services
from api.item.models import Item, ItemCreate

user_router = APIRouter()


@user_router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return services.create_user(db=db, user=user)


@user_router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip, limit)
    return users


@user_router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
