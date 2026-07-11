from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.patient import PatientModel
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter()


@router.post("/patients", response_model=PatientResponse)
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    new_patient = PatientModel(
        first_name=patient.first_name,
        last_name=patient.last_name,
        phone=patient.phone,
        national_code=patient.national_code,
        birth_date=patient.birth_date,
        gender=patient.gender,
        address=patient.address
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/patients", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientModel).all()

    return patients