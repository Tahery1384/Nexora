from fastapi import FastAPI

from app.api.patient import router as patient_router
from app.database.connection import engine
from app.database.base import Base

# همه مدل‌ها را import می‌کنیم تا SQLAlchemy آن‌ها را بشناسد
from app.models.patient import PatientModel

app = FastAPI()

# ساخت جدول‌ها
Base.metadata.create_all(bind=engine)

app.include_router(patient_router)


@app.get("/")
def home():
    return {"message": "Welcome to Nexora Clinic 🚀"}