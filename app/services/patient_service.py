from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.patient import PatientModel
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:

    @staticmethod
    def create_patient(patient: PatientCreate, db: Session):
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

    @staticmethod
    def get_patients(db: Session):
        return db.query(PatientModel).all()

    @staticmethod
    def get_patient(patient_id: int, db: Session):
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

    @staticmethod
    def update_patient(
        patient_id: int,
        patient: PatientUpdate,
        db: Session
    ):
        db_patient = PatientService.get_patient(
            patient_id,
            db
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

    @staticmethod
    def delete_patient(
        patient_id: int,
        db: Session
    ):
        patient = PatientService.get_patient(
            patient_id,
            db
        )

        db.delete(patient)
        db.commit()

        return {
            "message": "Patient deleted successfully"
        }