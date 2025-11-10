from typing import Optional
from pydantic import BaseModel


class DoctorCreate(BaseModel):
    user_id: int
    specialization: str
    office_number: str
    schedule: str
    department_id: Optional[int]
    is_chief: bool