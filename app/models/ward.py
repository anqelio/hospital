from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Ward(SQLModel, table=True):
    ward_id: Optional[int] = Field(default=None, primary_key=True)
    number: str
    department_id: int = Field(foreign_key="department.department_id")
    gender_type: str