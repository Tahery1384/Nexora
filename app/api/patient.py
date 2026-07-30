from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientPatch,
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
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return PatientService.get_patients(
        db=db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


@router.get("/patients/search", response_model=list[PatientResponse])
def search_patients(
    national_code: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone: Optional[str] = None,
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return PatientService.search_patients(
        db=db,
        national_code=national_code,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        gender=gender,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


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
@router.patch("/patients/{patient_id}", response_model=PatientResponse)
def patch_patient(
    patient_id: int,
    patient: PatientPatch,
    db: Session = Depends(get_db)
):
    return PatientService.patch_patient(
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