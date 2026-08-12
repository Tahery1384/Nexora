from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService


router = APIRouter()


@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.create_user(
        user=user,
        db=db
    )


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return UserService.login_user(
        user=user,
        db=db
    )