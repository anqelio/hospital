from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    patient_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    date_of_birth: date
    gender: str
    address: Optional[str] = None
    phone: Optional[str] = None
    ward_id: Optional[int] = Field(default=None, foreign_key="ward.ward_id")
    attending_doctor_id: Optional[int] = Field(default=None, foreign_key="doctor.doctor_id")
    date_start: datetime = Field(default_factory=datetime.utcnow)
    date_end: Optional[datetime] = None
    status: str = Field(default="active")