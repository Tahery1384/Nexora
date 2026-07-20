from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)
from app.services.patient_service import PatientService

router = APIRouter()


@router.post("/patients", response_model=PatientResponse)
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    return PatientService.create_patient(patient, db)


@router.get("/patients", response_model=list[PatientResponse])
def get_patients(
    db: Session = Depends(get_db)
):
    return PatientService.get_patients(db)


@router.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    return PatientService.get_patient(
        patient_id,
        db
    )


@router.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    return PatientService.update_patient(
        patient_id,
        patient,
        db
    )


@router.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    return PatientService.delete_patient(
        patient_id,
        db
    )