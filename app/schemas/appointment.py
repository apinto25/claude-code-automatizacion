from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    location: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.pending


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[AppointmentStatus] = None


class AppointmentResponse(AppointmentBase):
    id: int

    model_config = {"from_attributes": True}
