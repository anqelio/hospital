from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class DailyRecord(SQLModel, table=True):
    daily_record_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.patient_id")
    doctor_id: int = Field(foreign_key="doctor.doctor_id")
    record_date: date
    subjective_data: Optional[str] = None
    plan: Optional[str] = None