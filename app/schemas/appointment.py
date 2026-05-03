from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    location: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.pending
    duration: int = 30

    @field_validator('duration')
    @classmethod
    def duration_must_be_multiple_of_15(cls, v: int) -> int:
        if v % 15 != 0:
            raise ValueError('duration must be a multiple of 15 minutes')
        return v


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    duration: Optional[int] = None

    @field_validator('duration')
    @classmethod
    def duration_must_be_multiple_of_15(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v % 15 != 0:
            raise ValueError('duration must be a multiple of 15 minutes')
        return v


class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
