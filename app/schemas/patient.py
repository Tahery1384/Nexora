from pydantic import BaseModel, Field


class Patient(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=11, max_length=11)
    national_code: str = Field(..., min_length=10, max_length=10)
    birth_date: str
    gender: str
    address: str