from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.patient import PatientModel
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientPatch
)


class PatientService:

    @staticmethod
    def create_patient(
       patient: PatientCreate,
       db: Session
    ):
       existing_patient = (
           db.query(PatientModel)
           .filter(
               PatientModel.national_code == patient.national_code
           )
           .first()
       )

       if existing_patient:
           raise HTTPException(
               status_code=409,
               detail="Patient with this national code already exists"
           )

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
    def get_patients(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order: str = "asc"
    ):
     query = db.query(PatientModel)

     if hasattr(PatientModel, sort_by):
        column = getattr(PatientModel, sort_by)

        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        return (
         query
         .offset(skip)
         .limit(limit)
         .all()
        )


    @staticmethod
    def search_patients(
        db: Session,
        national_code: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        gender: str = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order: str = "asc"
    ):
        query = db.query(PatientModel)

        if national_code:
            query = query.filter(
                PatientModel.national_code == national_code
            )

        if first_name:
            query = query.filter(
                PatientModel.first_name.ilike(
                    f"%{first_name}%"
                )
            )

        if last_name:
            query = query.filter(
                PatientModel.last_name.ilike(
                    f"%{last_name}%"
                )
            )

        if phone:
            query = query.filter(
                PatientModel.phone == phone
            )
        if gender:
            query = query.filter(
                PatientModel.gender == gender
            )

        if hasattr(PatientModel, sort_by):
          column = getattr(PatientModel, sort_by)

        if order.lower() == "desc":
          query = query.order_by(column.desc())
        else:
           query = query.order_by(column.asc())

        return (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_patients(
       db: Session,
       skip: int = 0,
       limit: int = 10,
       sort_by: str = "id",
       order: str = "asc"
    ):
       query = db.query(PatientModel)

       if hasattr(PatientModel, sort_by):
          column = getattr(PatientModel, sort_by)

       if order.lower() == "desc":
        query = query.order_by(column.desc())
       else:
        query = query.order_by(column.asc())

       return (
         query
         .offset(skip)
         .limit(limit)
         .all()
        )

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
    def patch_patient(
        patient_id: int,
        patient: PatientPatch,
        db: Session
    ):
        db_patient = PatientService.get_patient(
            patient_id,
            db
        )

        update_data = patient.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_patient, key, value)

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