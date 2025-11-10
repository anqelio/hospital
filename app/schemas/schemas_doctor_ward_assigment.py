from typing import Optional
from pydantic import BaseModel


class CreateDoctorWardAssignment(BaseModel):
    doctor_id: int
    ward_id: int