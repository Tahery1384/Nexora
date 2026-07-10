from fastapi import APIRouter
from app.schemas.patient import Patient

router = APIRouter()

patients = []

@router.get("/patients")
def get_patients():
    return patients

@router.post("/patients")
def add_patient(patient: Patient):
    new_patient = {
        "id": len(patients) + 1,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "phone": patient.phone,
        "national_code": patient.national_code,
        "birth_date": patient.birth_date,
        "gender": patient.gender,
        "address": patient.address
    }

    patients.append(new_patient)

    return {
        "message": "Patient added successfully",
        "patient": new_patient
    }