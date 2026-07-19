from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.patient import PatientModel
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)

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
    return db.query(PatientModel).all()


@router.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(PatientModel)
        .filter(PatientModel.id == patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    db_patient = (
        db.query(PatientModel)
        .filter(PatientModel.id == patient_id)
        .first()
    )

    if db_patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db_patient.first_name = patient.first_name
    db_patient.last_name = patient.last_name
    db_patient.phone = patient.phone
    db_patient.national_code = patient.national_code
    db_patient.birth_date = patient.birth_date
    db_patient.gender = patient.gender
    db_patient.address = patient.address

    db.commit()
    db.refresh(db_patient)

    return db_patient


@router.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(PatientModel)
        .filter(PatientModel.id == patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }