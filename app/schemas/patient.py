from typing import Optional 
import re

from pydantic import BaseModel, Field, field_validator


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=11, max_length=11)
    national_code: str = Field(..., min_length=10, max_length=10)
    birth_date: str
    gender: str
    address: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("شماره تلفن باید فقط شامل عدد باشد")

        if len(value) != 11:
            raise ValueError("شماره تلفن باید ۱۱ رقم باشد")

        if not value.startswith("09"):
            raise ValueError("شماره تلفن باید با 09 شروع شود")

        return value

    @field_validator("national_code")
    @classmethod
    def validate_national_code(cls, value):
        if not value.isdigit():
            raise ValueError("کد ملی باید فقط شامل عدد باشد")

        if len(value) != 10:
            raise ValueError("کد ملی باید ۱۰ رقم باشد")

        if len(set(value)) == 1:
            raise ValueError("کد ملی معتبر نیست")

        check_digit = int(value[9])

        total = sum(
            int(value[i]) * (10 - i)
            for i in range(9)
        )

        remainder = total % 11

        if remainder < 2:
            valid = check_digit == remainder
        else:
            valid = check_digit == 11 - remainder

        if not valid:
            raise ValueError("کد ملی معتبر نیست")

        return value


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class PatientPatch(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    national_code: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None


class PatientResponse(PatientBase):
    id: int

    model_config = {
        "from_attributes": True
    }