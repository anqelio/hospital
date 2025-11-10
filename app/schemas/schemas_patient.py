from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    address: Optional[str]
    phone: Optional[str]
    ward_id: Optional[int]
    attending_doctor_id: Optional[int]
    date_start: datetime
    date_end: Optional[datetime]
    status: str