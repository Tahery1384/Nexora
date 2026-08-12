from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import UserModel
from app.schemas.user import UserCreate, UserLogin


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class UserService:

    @staticmethod
    def create_user(
        user: UserCreate,
        db: Session
    ):
        existing_user = (
            db.query(UserModel)
            .filter(
                UserModel.username == user.username
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        hashed_password = pwd_context.hash(
            user.password
        )

        new_user = UserModel(
            username=user.username,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login_user(
        user: UserLogin,
        db: Session
    ):
        db_user = (
            db.query(UserModel)
            .filter(
                UserModel.username == user.username
            )
            .first()
        )

        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        if not pwd_context.verify(
            user.password,
            db_user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "message": "Login successful",
            "username": db_user.username
        }