from typing import Optional
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str]
    head_doctor_id: Optional[int]