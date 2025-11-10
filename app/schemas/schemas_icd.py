from typing import Optional
from pydantic import BaseModel


class CreateICD(BaseModel):
    code: str
    description: str