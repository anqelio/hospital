from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class DoctorWardAssignment(SQLModel, table=True):
    doctor_ward_assigment_id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.doctor_id")
    ward_id: int = Field(foreign_key="ward.ward_id")