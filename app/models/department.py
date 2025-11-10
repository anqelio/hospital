from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Department(SQLModel, table=True):
    department_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    head_doctor_id: Optional[int] = Field(default=None, foreign_key="doctor.doctor_id")