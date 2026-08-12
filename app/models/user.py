from sqlalchemy import Column, Integer, String

from app.database.base import Base


class UserModel(Base):
    __tablename__= "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )