from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReferralCreate(BaseModel):
    patient_id: int
    attending_doctor_id: int
    reason: str
    referral_date: datetime
    is_completed: bool