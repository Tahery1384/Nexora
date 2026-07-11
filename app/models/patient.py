from sqlalchemy import Column, Integer, String

from app.database.base import Base


class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String)

    last_name = Column(String)

    phone = Column(String)

    national_code = Column(String)

    birth_date = Column(String)

    gender = Column(String)

    address = Column(String)