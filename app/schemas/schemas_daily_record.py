from datetime import date
from typing import Optional
from pydantic import BaseModel


class CreateDailyRecord(BaseModel):
    patient_id: int
    doctor_id: int
    record_date: date
    subjective_data: Optional[str]
    plan: Optional[str]