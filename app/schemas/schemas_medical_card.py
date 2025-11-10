from typing import Optional
from pydantic import BaseModel


class MedicalRecordCreate(BaseModel):
    patient_id: int
    diagnosis: Optional[str]
    icd_id: Optional[int]
    complaints: Optional[str]
    treatment: Optional[str]
    outcomes: Optional[str]
    created_by: int