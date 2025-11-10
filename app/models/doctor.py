from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Doctor(SQLModel, table=True):
    doctor_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    specialization: str
    office_number: str
    schedule: str
    department_id: Optional[int] = Field(default=None, foreign_key="department.department_id")
    is_chief: bool = Field(default=False)