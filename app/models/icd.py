from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ICD(SQLModel, table=True):
    icd_id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True)
    description: str