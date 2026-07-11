from pydantic import BaseModel, Field, field_validator


class Patient(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: str
    national_code: str
    birth_date: str
    gender: str
    address: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if len(value) != 11:
            raise ValueError("شماره موبایل باید ۱۱ رقم باشد.")

        if not value.startswith("09"):
            raise ValueError("شماره موبایل باید با 09 شروع شود.")

        if not value.isdigit():
            raise ValueError("شماره موبایل فقط باید شامل عدد باشد.")

        return value

    @field_validator("national_code")
    @classmethod
    def validate_national_code(cls, value):
        if len(value) != 10:
            raise ValueError("کد ملی باید ۱۰ رقم باشد.")

        if not value.isdigit():
            raise ValueError("کد ملی فقط باید شامل عدد باشد.")

        check = int(value[9])

        total = 0
        for i in range(9):
            total += int(value[i]) * (10 - i)

        remainder = total % 11

        if remainder < 2:
            if check != remainder:
                raise ValueError("کد ملی معتبر نیست.")
        else:
            if check != (11 - remainder):
                raise ValueError("کد ملی معتبر نیست.")

        return value