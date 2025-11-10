from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class MedicalRecord(SQLModel, table=True):
    medical_record_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.patient_id")
    diagnosis: Optional[str] = None
    icd_id: Optional[int] = Field(default=None, foreign_key="icd.icd_id")
    complaints: Optional[str] = None
    treatment: Optional[str] = None
    outcomes: Optional[str] = None
    created_by: int = Field(foreign_key="user.user_id")