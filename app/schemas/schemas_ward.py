from typing import Optional
from pydantic import BaseModel

class WardCreate(BaseModel):
    number: str
    department_id: int
    gender_type: str