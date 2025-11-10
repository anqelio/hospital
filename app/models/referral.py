from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Referral(SQLModel, table=True):
    referral_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.patient_id")
    attending_doctor_id: int = Field(foreign_key="doctor.doctor_id")
    reason: str
    referral_date: datetime = Field(default_factory=datetime.utcnow)
    is_completed: bool = Field(default=False)